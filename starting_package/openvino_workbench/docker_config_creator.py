"""
 OpenVINO DL Workbench Python Starter
 Functions for the Docker config creation

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
import os
import platform
import random
import string
import sys
from argparse import Namespace
from pathlib import Path

from openvino_workbench.constants import (DL_WB_DOCKER_CONFIG_PATH,
                                          INTERNAL_PORT,
                                          ABORTING_EXIT_MESSAGE,
                                          CLI_COMMAND,
                                          LOGGER_NAME)


class DockerConfigCreator:
    def __init__(self, arguments: Namespace):
        self._arguments = arguments
        self._logger = logging.getLogger(LOGGER_NAME)
        self.config = {}
        self._user_os = platform.system()
        self._create_config()

    def _create_config(self) -> dict:
        # Get OS
        self._logger.debug(f'OS: {self._user_os}.')

        self.config = {'image': f'{self._arguments.image}',
                       'environment': {'PUBLIC_PORT': self._arguments.port,
                                       'SSL_VERIFY': 'on' if self._arguments.verify_ssl else 'off',
                                       'BASE_PREFIX': self._arguments.base_prefix,
                                       'NETWORK_ALIAS': self._arguments.network_alias,
                                       'PYTHON_WRAPPER': 1},
                       'name': self._arguments.container_name,
                       'ports': {INTERNAL_PORT: (self._arguments.ip, self._arguments.port)},
                       'hostname': self._arguments.network_alias,
                       'stderr': True,
                       'stdout': True,
                       'detach': True,
                       'tty': True}

        # Authentication
        if self._arguments.enable_authentication:
            self.config['environment']['ENABLE_AUTH'] = 1

            if self._arguments.custom_token:
                self.config['environment']['CUSTOM_TOKEN'] = self._arguments.custom_token

            if self._arguments.disable_token_saving:
                self.config['environment']['SAVE_TOKEN_TO_FILE'] = 0

        # Jupyter
        if self._arguments.no_jupyter:
            self.config['environment']['DISABLE_JUPYTER'] = 1

        # Proxies
        if self._arguments.http_proxy:
            self.config['environment']['http_proxy'] = self._arguments.http_proxy
        if self._arguments.https_proxy:
            self.config['environment']['https_proxy'] = self._arguments.https_proxy
        if self._arguments.no_proxy:
            self.config['environment']['no_proxy'] = self._arguments.no_proxy

        # MYRIAD & HDDL
        if self._arguments.enable_myriad:
            if 'volumes' not in self.config:
                self.config['volumes'] = {}
            self.config['volumes']['/dev/bus/usb'] = {'bind': '/dev/bus/usb', 'mode': 'rw'}
            self.config['device_cgroup_rules'] = ['c 189:* rmw']
        elif self._arguments.enable_hddl:
            self._check_hddl_daemon_is_running()
            self._add_hddl_specific_params()

        # GPU
        if self._arguments.enable_gpu:
            self._add_gpu_specific_params()

        # Mount assets directory
        if self._arguments.assets_directory:

            assets_directory: str = self._check_and_transform_assets_directory()

            if 'volumes' in self.config:
                self.config['volumes'][assets_directory] = {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
            else:
                self.config['volumes'] = {
                    assets_directory: {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
                }

            # SSL
            if self._arguments.ssl_certificate_name:
                if not self._are_ssl_files_present_in_assets_directory():
                    self._logger.debug(
                        'SSL key or/and SSL certificate files are not present in the provided directory.')
                    self._logger.info(
                        'ERROR: SSL key or/and SSL certificate files are not present in the provided directory: '
                        f'{self._arguments.assets_directory}. Place them there and try again.'
                        f'{ABORTING_EXIT_MESSAGE}')
                    sys.exit(1)

                self.config['environment']['SSL_KEY'] = os.path.join(DL_WB_DOCKER_CONFIG_PATH,
                                                                     self._arguments.ssl_key_name)
                self.config['environment']['SSL_CERT'] = os.path.join(DL_WB_DOCKER_CONFIG_PATH,
                                                                      self._arguments.ssl_certificate_name)

        # DevCloud
        if self._arguments.cloud_service_address:
            self.config['environment']['CLOUD_SERVICE_URL'] = self._arguments.cloud_service_address
            self.config['network'] = self._arguments.network_name
        if self._arguments.cloud_service_session_ttl:
            self.config['environment']['CLOUD_SERVICE_SESSION_TTL_MINUTES'] = self._arguments.cloud_service_session_ttl

        self._logger.debug(f'Created config: {self.config}.')

    def _check_and_transform_assets_directory(self) -> str:
        if not os.path.isabs(self._arguments.assets_directory):
            self._logger.debug('Assets directory is not absolute.')
            self._logger.info(
                f'WARNING: Provided assets directory path: "{self._arguments.assets_directory}" is not absolute.\n'
                'Make sure that it is relative to the folder from which you use the starter. '
                'If the folder is not mounted or the container does not start, try using the absolute path.\n')
            work_dir = os.path.abspath(os.getcwd())
            self._arguments.assets_directory = os.path.join(work_dir, self._arguments.assets_directory)

        if not os.path.isdir(self._arguments.assets_directory):
            self._logger.debug('Assets directory does not exist.')
            self._logger.info(
                f'ERROR: Provided assets directory: "{self._arguments.assets_directory}" does not exist. Correct '
                f'the path or create a '
                'directory and use it with the "--assets-directory" argument.'
                f'{ABORTING_EXIT_MESSAGE}')
            sys.exit(1)

        if not self._is_dir_writable():
            if self._user_os == 'Linux':
                self._logger.info(f'ERROR: Provided assets directory: "{self._arguments.assets_directory}" '
                                  'does not have required permissions. '
                                  'Read, write, and execute permissions are required for the "others" group (at least '
                                  '**7 mode). '
                                  'Create the required configuration directory with the following command: '
                                  '\n\n\tmkdir -p -m 777 /path/to/directory'
                                  '\n\nThen copy the required assets into it and use it: '
                                  f'\n\n\t{CLI_COMMAND} --assets-directory /path/to/directory'
                                  f'{ABORTING_EXIT_MESSAGE}')
            else:
                self._logger.info(
                    f'ERROR: Provided assets directory: {self._arguments.assets_directory} is not writable.'
                    '\nCheck that the directory has writing permissions and try again.'
                    f'{ABORTING_EXIT_MESSAGE}')
            sys.exit(1)

        return self._arguments.assets_directory

    def _is_dir_writable_linux(self) -> bool:
        permissions = oct(os.stat(self._arguments.assets_directory).st_mode)[-1]
        return permissions == '7'

    def _is_dir_writable_general(self) -> bool:
        test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + 'text.txt'  # nosec
        try:
            with open(os.path.join(self._arguments.assets_directory, test_file_name), 'w') as filehandler:
                filehandler.write('Sample file.')
        except IOError:
            return False
        os.remove(os.path.join(self._arguments.assets_directory, test_file_name))
        return True

    def _is_dir_writable(self) -> bool:
        if self._user_os == 'Linux':
            return self._is_dir_writable_linux()

        return self._is_dir_writable_general()

    def _are_ssl_files_present_in_assets_directory(self) -> bool:
        return os.path.isfile(
            os.path.join(self._arguments.assets_directory, self._arguments.ssl_certificate_name)) and os.path.isfile(
            os.path.join(self._arguments.assets_directory, self._arguments.ssl_key_name))

    def _add_device_to_config(self, device: str, mode: str = 'rmw'):
        device_mount_string = f'{device}:{device}:{mode}'
        if 'devices' not in self.config:
            self.config['devices'] = [device_mount_string]
        else:
            self.config['devices'].append(device_mount_string)

    def _add_hddl_specific_params(self):
        ion_device = Path('/dev/ion')
        if ion_device.exists():
            self._add_device_to_config('/dev/ion')

        self.config['volumes'] = {
            '/var/tmp': {'bind': '/var/tmp', 'mode': 'rw'},  # nosec
            '/dev/shm': {'bind': '/dev/shm', 'mode': 'rw'}  # nosec
        }

    def _add_gpu_specific_params(self):
        if 'group_add' not in self.config:
            self.config['group_add'] = []
        for group_name in ('video', 'render'):
            try:
                group_id = self._get_group_id(group_name)
            except AssertionError as error:
                self._logger.info(error)
                continue

            self.config['group_add'].append(group_id)
        self._add_device_to_config('/dev/dri')

    @staticmethod
    def _get_group_id(group: str) -> int:
        import grp
        try:
            return grp.getgrnam(group).gr_gid
        except KeyError as no_group_error:
            raise AssertionError(f'WARNING: There is no "{group}" group on the machine. '
                                 'GPU might not be available for inference.') from no_group_error

    def _check_hddl_daemon_is_running(self):
        import psutil
        if 'hddldaemon' not in (process.name() for process in psutil.process_iter()):
            self._logger.info('WARNING: "hddldaemon" was not found running in the background.'
                              'HDDL might not be available.')
