"""
 OpenVINO Profiler
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

import os
import platform
import random
import string
import sys
from argparse import Namespace
from pathlib import Path

from openvino_workbench.constants import DL_WB_DOCKER_CONFIG_PATH


def does_dir_exist(path_to_dir: str) -> bool:
    return os.path.isdir(path_to_dir)


def check_for_assets_dir(path_to_dir: str):
    if not does_dir_exist(path_to_dir):
        print(f'Provided assets directory: "{path_to_dir}" does not exist.\n'
              'Aborting.')
        sys.exit(1)


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


def are_args_valid_for_windows(args: Namespace) -> bool:
    return not ((args.enable_myriad or args.enable_hddl or args.enable_gpu) and platform.system() == 'Windows')


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
    except KeyError:
        raise AssertionError(f'There is no "{group}" group on the machine. '
                             'GPU might not be available for inference.')


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


def create_config_for_container(passed_arguments: Namespace) -> dict:
    # Get OS
    user_os = platform.system()

    config = {'image': f'{passed_arguments.image}',
              'environment': {'PUBLIC_PORT': passed_arguments.port,
                              'SSL_VERIFY': 'on' if passed_arguments.verify_ssl else 'off',
                              'BASE_PREFIX': passed_arguments.base_prefix,
                              'NETWORK_ALIAS': passed_arguments.network_alias,
                              'PYTHON_WRAPPER': 1},
              'name': passed_arguments.container_name,
              'hostname': passed_arguments.ip,
              'ports': {'5665': passed_arguments.port},
              'stderr': True,
              'stdout': True,
              'detach': True,
              'tty': True}

    # Authentication
    if passed_arguments.enable_authentication:
        config['environment']['ENABLE_AUTH'] = 1

    # Jupyter
    if passed_arguments.no_jupyter:
        config['environment']['DISABLE_JUPYTER'] = 1

    # Proxies
    if passed_arguments.http_proxy:
        config['environment']['http_proxy'] = passed_arguments.http_proxy
    if passed_arguments.https_proxy:
        config['environment']['https_proxy'] = passed_arguments.https_proxy
    if passed_arguments.no_proxy:
        config['environment']['no_proxy'] = passed_arguments.no_proxy

    # Devices
    if not are_args_valid_for_windows(passed_arguments):
        print('DL Workbench does not support non-CPU (GPU, VPU, HDDL) devices on Windows.\n'
              'Please remove the non-CPU related arguments (--enable-gpu/--enable-myriad/--enable-hddl).\n'
              'Aborting.')
        sys.exit(1)

    # MYRIAD & HDDL
    if passed_arguments.enable_myriad:
        add_device_to_config(config, '/dev/bus/usb')
        config['device_cgroup_rules'] = ['c 189:* rmw']
    elif passed_arguments.enable_hddl:
        check_hddl_daemon_is_running()
        add_hddl_specific_params(config)

    # GPU
    if passed_arguments.enable_gpu:
        add_gpu_specific_params(config)

    # Mount assets directory
    if passed_arguments.assets_directory:

        check_for_assets_dir(passed_arguments.assets_directory)

        if not is_dir_writable(passed_arguments.assets_directory, user_os):
            print_not_writable_dir_message(user_os, passed_arguments.assets_directory)
            print('Aborting.')
            sys.exit(1)

        if 'volumes' in config:
            config['volumes'][passed_arguments.assets_directory] = {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
        else:
            config['volumes'] = {
                passed_arguments.assets_directory: {'bind': DL_WB_DOCKER_CONFIG_PATH, 'mode': 'rw'}
            }

        # SSL
        if passed_arguments.ssl_certificate_name:
            if not are_ssl_files_present_in_assets_dir(passed_arguments.ssl_certificate_name,
                                                       passed_arguments.ssl_key_name,
                                                       passed_arguments.assets_directory):
                print(f'SSL Key or/and SSL Certificate files are not present in the provided directory: '
                      f'{passed_arguments.assets_directory}.')
                print('Aborting.')
                sys.exit(1)

            config['environment']['SSL_KEY'] = os.path.join(DL_WB_DOCKER_CONFIG_PATH,
                                                            passed_arguments.ssl_certificate_name)
            config['environment']['SSL_CERT'] = os.path.join(DL_WB_DOCKER_CONFIG_PATH,
                                                             passed_arguments.ssl_key_name)

    # DevCloud
    if passed_arguments.cloud_service_address:
        config['environment']['CLOUD_SERVICE_URL'] = passed_arguments.cloud_service_address
    if passed_arguments.cloud_service_session_ttl:
        config['environment']['CLOUD_SERVICE_SESSION_TTL_MINUTES'] = passed_arguments.cloud_service_session_ttl

    return config
