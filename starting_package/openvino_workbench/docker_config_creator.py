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

from openvino_workbench.constants import DL_WB_DOCKER_CONFIG_PATH, INTERNAL_PORT


class DockerConfigCreator:
    def __init__(self, arguments: Namespace, logger: logging.Logger):
        self._arguments = arguments
        self._logger = logger
        self.config = {}
        self._create_config()

    def _create_config(self) -> dict:
        # Get OS
        user_os = platform.system()
        self._logger.info(f'OS: {user_os}.')

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
            add_device_to_config(self.config, '/dev/bus/usb')
            self.config['device_cgroup_rules'] = ['c 189:* rmw']
        elif self._arguments.enable_hddl:
            check_hddl_daemon_is_running()
            add_hddl_specific_params(self.config)

        # GPU
        if self._arguments.enable_gpu:
            add_gpu_specific_params(self.config)

        # Mount assets directory
        if self._arguments.assets_directory:

            assets_directory: str = check_and_transform_assets_dir(self._arguments.assets_directory, user_os)

            if 'volumes' in self.config:
                self.config['volumes'][assets_directory] = {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
            else:
                self.config['volumes'] = {
                    assets_directory: {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
                }

            # SSL
            if self._arguments.ssl_certificate_name:
                if not are_ssl_files_present_in_assets_dir(self._arguments.ssl_certificate_name,
                                                           self._arguments.ssl_key_name,
                                                           assets_directory):
                    self._logger.info('SSL key or/and SSL certificate files are not present in the provided directory.')
                    print(f'SSL key or/and SSL certificate files are not present in the provided directory: '
                          f'{self._arguments.assets_directory}.')
                    print('Aborting.')
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

        self._logger.info(f'Created config: {self.config}.')

    def check_and_transform_assets_dir(self, path_to_dir: str, user_os: str) -> str:
        if not os.path.isabs(path_to_dir):
            print(f'WARNING: Provided assets directory path: "{path_to_dir}" is not absolute.\n'
                  'Make sure that it is relative to the folder from which you use the starter. '
                  'If the folder is not mounted or the container does not start, try using the absolute path.\n')
            work_dir = os.path.abspath(os.getcwd())
            path_to_dir = os.path.join(work_dir, path_to_dir)

        if not os.path.isdir(path_to_dir):
            print(f'Provided assets directory: "{path_to_dir}" does not exist.\n'
                  'Aborting.')
            sys.exit(1)

        if not is_dir_writable(path_to_dir, user_os):
            print_not_writable_dir_message(user_os, path_to_dir)
            print('Aborting.')
            sys.exit(1)

        return path_to_dir


def is_dir_writable_linux(path_to_dir: str) -> bool:
    permissions = oct(os.stat(path_to_dir).st_mode)[-1]
    return permissions == '7'


def is_dir_writable_general(path_to_dir: str) -> bool:
    test_file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)) + 'text.txt'
    try:
        with open(os.path.join(path_to_dir, test_file_name), 'w') as filehandler:
            filehandler.write('Sample file.')
    except IOError:
        return False
    os.remove(os.path.join(path_to_dir, test_file_name))
    return True


def is_dir_writable(path_to_dir: str, os_name: str) -> bool:
    if os_name == 'Linux':
        return is_dir_writable_linux(path_to_dir)

    return is_dir_writable_general(path_to_dir)


def are_ssl_files_present_in_assets_dir(ssl_cert_name: str, ssl_key_name: str, assets_dir: str) -> bool:
    return os.path.isfile(os.path.join(assets_dir, ssl_cert_name)) and os.path.isfile(
        os.path.join(assets_dir, ssl_key_name))


def add_device_to_config(config: dict, device: str, mode: str = 'rmw'):
    device_mount_string = f'{device}:{device}:{mode}'
    if 'devices' not in config:
        config['devices'] = [device_mount_string]
    else:
        config['devices'].append(device_mount_string)


def add_hddl_specific_params(config: dict):
    ion_device = Path('/dev/ion')
    if ion_device.exists():
        add_device_to_config(config, '/dev/ion')

    config['volumes'] = {
        '/var/tmp': {'bind': '/var/tmp', 'mode': 'rw'},  # nosec
        '/dev/shm': {'bind': '/dev/shm', 'mode': 'rw'}  # nosec
    }


def add_gpu_specific_params(config: dict):
    if 'group_add' not in config:
        config['group_add'] = []
    for group_name in ('video', 'render'):
        try:
            group_id = get_group_id(group_name)
        except AssertionError as error:
            print(error)
            continue

        config['group_add'].append(group_id)
    add_device_to_config(config, '/dev/dri')


def get_group_id(group: str) -> int:
    import grp
    try:
        return grp.getgrnam(group).gr_gid
    except KeyError as no_group_error:
        raise AssertionError(f'There is no "{group}" group on the machine. '
                             'GPU might not be available for inference.') from no_group_error


def check_hddl_daemon_is_running():
    import psutil
    if 'hddldaemon' not in (process.name() for process in psutil.process_iter()):
        print('"hddldaemon" was not found running in the background.'
              'HDDL might not be available.')


def print_not_writable_dir_message(user_os: str, dir_path: str):
    if user_os == 'Linux':
        print(f'''Provided assets directory: "{dir_path}"
does not have required permissions. 
Read, write, and execute permissions are required for 'others' group (at least **7 mode).
Create the required configuration directory with the following command: 

mkdir -p -m 777 /path/to/dir

Then copy the required assets into it and and mount the directory by assigning it to the '--assets-directory' argument.
''')
    else:
        print(f'Cannot write into: {dir_path}.\n'
              'Check that directory has writing permissions.')
