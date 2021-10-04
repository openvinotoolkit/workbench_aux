"""
 OpenVINO Profiler
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

import sys

from tqdm import tqdm

from openvino_workbench.constants import DOCKER_HUB_TAGS_URL
from openvino_workbench.utils import get_image_size

from docker import DockerClient


def extract_progress_info(line: dict) -> dict:
    total_weight = 0
    current = 0

    pid = line.get('id', '')
    status = line.get('status', '')
    progress_detail = line.get('progressDetail', {})

    if progress_detail:
        current = line['progressDetail']['current']
        total_weight = line['progressDetail']['total']

    # Create progress object
    progress = {'id': pid, 'status': status,
                'total_layer_weight': total_weight,
                'current': current}

    return progress


def calculate_total_progress(total_downloaded: int, total_extracted: int, total_image_size: int) -> int:
    return int(0.5 * (total_downloaded + total_extracted) / total_image_size * 100)


def update_progress_bar(progress: int, progress_bar: tqdm):
    progress_bar.update(progress - progress_bar.n)


def parse_image_name(image_name: str) -> tuple:
    try:
        repository, tag = image_name.split(':')
    except ValueError:
        print(f'The specified image name: "{image_name}" might be incorrect.\n'
              f'Please specify the image name in the following format: repository:tag\n'
              f'Example: openvino/workbench:latest\n'
              f'Or omit the `--image` argument to use the latest version of DL Workbench.\n'
              f'Aborting.')
        sys.exit(1)
    return repository, tag


def is_image_present(docker_client: DockerClient, repository_to_search: str, tag_to_search: str) -> bool:
    if not docker_client.images.list(name=repository_to_search):
        return False

    for image in docker_client.images.list(name=repository_to_search):
        if not image.attrs['RepoTags']:
            continue
        repository, tag = parse_image_name(image.attrs['RepoTags'][0])
        if repository == repository_to_search and tag == tag_to_search:
            return True
    return False


def is_image_present_in_registry(docker_client: DockerClient, image_name: str) -> bool:
    try:
        # If the image exists, this will not raise an error and return non-empty object
        return bool(docker_client.images.get_registry_data(image_name))
    # Raises error otherwise
    except Exception:
        return False


def pull_image_without_progress(docker_client: DockerClient, repository: str, tag: str):
    print('Pulling image...')
    docker_client.api.pull(repository=repository, tag=tag)
    print('Pull is complete.')


def pull_image_and_display_progress(docker_client: DockerClient, image_name: str, proxies: dict,
                                    force_pull: bool = False):
    repository, tag = parse_image_name(image_name)

    if is_image_present(docker_client, repository, tag) and not force_pull:
        print(f'Specified image: {repository}:{tag} is present on the machine. Continuing with it...')
        print('NOTE: If you want to force-update your image, add `--force-pull` argument.\n')
        return

    # Check if image is present in registry
    if not is_image_present_in_registry(docker_client, image_name):
        print(f'The specified image name: "{image_name}" might be incorrect.\n'
              f'Could not found the image in the {repository} repository. Please check if the image name is correct\n'
              f'and is in the following format: repository:tag\n'
              f'Example: openvino/workbench:latest\n'
              f'Or omit the `--image` argument to use the latest version of DL Workbench.\n'
              f'Aborting.')
        sys.exit(1)

    # Get image size
    total_image_size = get_image_size(DOCKER_HUB_TAGS_URL, proxies)
    if not total_image_size:
        print('Could not get image size from Docker Hub, pulling without displaying progress.')
        pull_image_without_progress(docker_client, repository, tag)
        return

    # To keep track of current downloading/extraction
    # Structure example:
    # layers = {'id1': {'downloading': 1000, 'extracting': 2000},
    #           'id2': {'downloading': 500000, 'extracting': 1000000}}
    layers_info = {}

    bar_formatting = '{desc}: |{bar}|{percentage:3.0f}%. Elapsed Time: {elapsed}. Remaining (Estimated): {remaining}.'

    with tqdm(desc='Pulling Image', bar_format=bar_formatting, total=100, ncols=90, ascii=True) \
            as progress_bar:

        for line in docker_client.api.pull(repository=repository, tag=tag, stream=True, decode=True):
            result = extract_progress_info(line)
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

            progress_total = calculate_total_progress(total_downloaded, total_extracted, total_image_size)

            # Update progress bar
            if progress_total != progress_bar.last_print_n < 100:
                update_progress_bar(progress_total, progress_bar)

        # Last update if < 100
        update_progress_bar(progress_bar.total, progress_bar)

    print('\nPull is complete.')
