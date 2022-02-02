"""
 OpenVINO Profiler
 Utility functions

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
import platform
import sys

import docker
from openvino_workbench.constants import INTERNAL_PORT, LOGGER, LOG_FILE, COMMUNITY_LINK


def print_starting_message(config: dict, enabled_devices: dict, log_file: str):
    bound_ip, port = config['ports'][INTERNAL_PORT]
    print('\nStarting the DL Workbench with the following arguments:\n'
          f'Image Name: {config["image"]}\n'
          f'Container Name: {config["name"]}\n'
          f'IP: {bound_ip}\n'
          f'Port: {port}\n'
          f'GPU Enabled: {"True" if enabled_devices["GPU"] else "False"}\n'
          f'MYRIAD Enabled: {"True" if enabled_devices["MYRIAD"] else "False"}\n'
          f'HDDL Enabled: {"True" if enabled_devices["HDDL"] else "False"}\n'
          f'Path to the log file: {log_file}\n')


def initialize_docker_client(logger: logging.Logger) -> docker.DockerClient:
    try:
        client = docker.from_env()
        logger.info('Docker client is initialized.')
    except docker.errors.DockerException:
        logger.error('Docker client was not initialized.', exc_info=True)
        print('Could not initialize the Docker client from environment.')
        if platform.system() in ('Windows', 'Darwin'):
            print('Please check if the Docker Desktop is running.')
        else:
            print('Please check if the Docker daemon is running.')
        sys.exit(1)
    return client


def save_logs_on_failure(fnc):
    def decorated_func(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except Exception as error:
            LOGGER.error('Unexpected error occurred', exc_info=True)
            error_message = str(error)
            error_type = type(error)
            print(f'''* ERR: Unexpected error occurred!
* Error message: {error_message if error_type else None}
* Error type: {error_type}
* Complete log can be found at: {LOG_FILE}
* Please report this log to the: {COMMUNITY_LINK}
''')
            sys.exit(1)

    return decorated_func
