"""
 OpenVINO DL Workbench Python Starter
 Docker image-related logic

 Copyright (c) 2021 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""

import logging
import sys
from typing import Tuple

import requests
from docker import DockerClient
from openvino_workbench.constants import DOCKER_HUB_TAGS_URL, EXAMPLE_COMMAND, ABORTING_EXIT_MESSAGE, LOGGER_NAME
from tqdm import tqdm


class DockerImage:
    def __init__(self, docker_client: DockerClient, image_name: str, proxies=None):
        if proxies is None:
            proxies = {}
        self.client = docker_client
        self.image_name = image_name
        self.repository, self.tag = self._parse_image_name(self.image_name)
        self._logger = logging.getLogger(LOGGER_NAME)
        self.proxies = proxies
        self._is_present = self._is_image_present()
        self._is_present_in_registry = self._is_image_present_in_registry()

    def pull(self, force_pull: bool = False):
        self._logger.debug(f'Pulling image with the name: {self.image_name}')

        if self._is_present and not force_pull:
            self._logger.debug('Image is present on the machine.')
            self._logger.info(
                f'The specified image: {self.repository}:{self.tag} is present on the machine. Continuing with it...\n'
                'NOTE: If you want to force-update your image, add `--force-pull` argument.\n')
            return

        # Check if image is present in registry
        if not self._is_present_in_registry:
            self._logger.info(f'ERROR: The specified image name: "{self.image_name}" might be incorrect.'
                              f'\nCould not find the image in the {self.repository} repository.'
                              f'\nCheck if the image name is correct and has the following format: '
                              f'repository:tag '
                              f'{EXAMPLE_COMMAND}'
                              f'{ABORTING_EXIT_MESSAGE}')
            sys.exit(1)

        # Get image size
        total_image_size = self._get_image_size(DOCKER_HUB_TAGS_URL)
        if not total_image_size:
            self._logger.info('WARNING: Could not get the image size from Docker Hub, '
                              'pulling without displaying progress.')
            self._pull_image_without_progress()
            return

        # To keep track of current downloading/extraction
        # Structure example:
        # layers = {'id1': {'downloading': 1000, 'extracting': 2000},
        #           'id2': {'downloading': 500000, 'extracting': 1000000}}
        layers_info = {}

        bar_formatting = '{desc}: |{bar}|{percentage:3.0f}%. Elapsed Time: {elapsed}. Remaining (Estimated): {' \
                         'remaining}. '

        with tqdm(desc='Pulling Image', bar_format=bar_formatting, total=100, ncols=90, ascii=True) \
                as progress_bar:

            for line in self.client.api.pull(repository=self.repository, tag=self.tag, stream=True, decode=True):
                result = self._extract_progress_info(line)
                layer_id = result['id']

                if layer_id and layer_id not in layers_info:
                    layers_info[layer_id] = {'downloading': 0, 'extracting': 0}

                # Get current progress of layer pulling
                if result['status'] == 'Extracting':
                    layers_info[layer_id]['extracting'] = result['current']
                elif result['status'] == 'Downloading':
                    layers_info[layer_id]['downloading'] = result['current']

                # Calculate current progress
                total_downloaded = 0
                total_extracted = 0
                for statuses in layers_info.values():
                    total_downloaded += statuses['downloading']
                    total_extracted += statuses['extracting']

                progress_total = self._calculate_total_progress(total_downloaded, total_extracted, total_image_size)

                # Update progress bar
                if progress_total != progress_bar.last_print_n < 100:
                    self._update_progress_bar(progress_total, progress_bar)

            # Last update if < 100
            self._update_progress_bar(progress_bar.total, progress_bar)

        self._logger.debug('Image was pulled.')
        self._logger.info('\nPull is complete.')

    def _pull_image_without_progress(self):
        self._logger.debug(f'Pulling the image: {self.image_name} without progress bar.')
        self._logger.info('Pulling the image...')
        self.client.api.pull(repository=self.repository, tag=self.tag)
        self._logger.info('Pull is complete.')
        self._logger.debug('Image was pulled without progress.')

    def _parse_image_name(self, image_name: str) -> Tuple[str, str]:
        try:
            repository, tag = image_name.split(':')
        except ValueError:
            self._logger.error('Could not parse the image name.', exc_info=True)
            self._logger.info(f'ERROR: The specified image name: "{image_name}" might be incorrect.'
                              '\nSpecify the image name in the following format: repository:tag.'
                              f'{EXAMPLE_COMMAND}'
                              f'{ABORTING_EXIT_MESSAGE}')
            sys.exit(1)
        return repository, tag

    def _is_image_present(self) -> bool:
        if not self.client.images.list(name=self.repository):
            return False

        for image in self.client.images.list(name=self.repository):
            if not image.attrs['RepoTags']:
                continue
            repository, tag = self._parse_image_name(image.attrs['RepoTags'][0])
            if repository == self.repository and tag == self.tag:
                return True
        return False

    def _is_image_present_in_registry(self) -> bool:
        try:
            # If the image exists, this will not raise an error and return non-empty object
            return bool(self.client.images.get_registry_data(self.image_name))
        # Raises error otherwise
        except Exception:
            self._logger.error(f'Image with the name "{self.image_name}" was not found in registry.', exc_info=True)
            return False

    def _get_image_size(self, repository_tags_url: str) -> int:
        try:
            images_info = requests.get(repository_tags_url, proxies=self.proxies).json()
            return images_info['results'][0]['full_size']
        except Exception:
            self._logger.error(f'Could not get the image size from the Hub. Image {self.image_name}', exc_info=True)
            return 0

    @staticmethod
    def _extract_progress_info(pull_progress: dict) -> dict:
        total_weight = 0
        current = 0

        pid = pull_progress.get('id', '')
        status = pull_progress.get('status', '')
        progress_detail = pull_progress.get('progressDetail', {})

        # Need to check for 'current' and 'total' as first progress details might be empty yet present
        if progress_detail and 'current' in progress_detail and 'total' in progress_detail:
            current = pull_progress['progressDetail']['current']
            total_weight = pull_progress['progressDetail']['total']

        # Create progress object
        progress = {'id': pid, 'status': status,
                    'total_layer_weight': total_weight,
                    'current': current}

        return progress

    @staticmethod
    def _calculate_total_progress(total_downloaded: int, total_extracted: int, total_image_size: int) -> int:
        return int(0.5 * (total_downloaded + total_extracted) / total_image_size * 100)

    @staticmethod
    def _update_progress_bar(progress: int, progress_bar: tqdm):
        progress_bar.update(progress - progress_bar.n)
