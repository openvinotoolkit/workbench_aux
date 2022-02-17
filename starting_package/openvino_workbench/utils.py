"""
 OpenVINO DL Workbench Python Starter
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
import os
import platform
import re
import sys
from typing import Optional, Callable

import docker
from openvino_workbench.constants import INTERNAL_PORT, LOGGER, ABORTING_EXIT_MESSAGE, \
    DOCKER_ERROR_PATTERNS


def print_starting_message(config: dict, enabled_devices: dict, log_file: str):
    bound_ip, port = config['ports'][INTERNAL_PORT]
    docker_environment = config.get('environment', {})
    authentication_enabled = docker_environment.get('ENABLE_AUTH') == 1
    disable_token_saving = docker_environment.get('SAVE_TOKEN_TO_FILE') == 0
    token_saving_message = f'Token Saving To File Enabled: {"True" if not disable_token_saving else "False"}\n'
    is_custom_token_provided = bool(docker_environment.get('CUSTOM_TOKEN'))
    custom_token_message = f'Custom Token Provided: {"True" if is_custom_token_provided else "False"}\n'
    is_jupyter_disabled = docker_environment.get('DISABLE_JUPYTER') == 1
    starting_message = ('\nStarting the DL Workbench with the following arguments:\n'
                        f'Image Name: {config["image"]}\n'
                        f'Container Name: {config["name"]}\n'
                        f'IP: {bound_ip}\n'
                        f'Port: {port}\n'
                        f'GPU Enabled: {"True" if enabled_devices["GPU"] else "False"}\n'
                        f'MYRIAD Enabled: {"True" if enabled_devices["MYRIAD"] else "False"}\n'
                        f'HDDL Enabled: {"True" if enabled_devices["HDDL"] else "False"}\n'
                        f'Authentication Enabled: {"True" if authentication_enabled else "False"}\n'
                        f'{custom_token_message if authentication_enabled else ""}'
                        f'{token_saving_message if authentication_enabled else ""}'
                        f'Jupyter Enabled: {"True" if not is_jupyter_disabled else "False"}\n'
                        f'Path to the log file: {log_file}\n')
    LOGGER.info(starting_message)


def initialize_docker_client() -> docker.DockerClient:
    try:
        client = docker.from_env()
        LOGGER.debug('Docker client is initialized.')
    except docker.errors.DockerException:
        LOGGER.debug('Docker client was not initialized.', exc_info=True)
        LOGGER.info('Could not initialize the Docker client from environment.')
        if platform.system() in ('Windows', 'Darwin'):
            LOGGER.info('Please check if the Docker Desktop is running.')
        else:
            LOGGER.info('Please check if the Docker daemon is running.')
        sys.exit(1)
    return client


def save_logs_on_failure(fnc) -> Callable:
    def decorated_func(*args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except Exception as error:
            error_message = parse_error(str(error))
            LOGGER.debug(error_message, exc_info=True)

            error_message = (f'\nERROR: {error_message}.'
                             f'{ABORTING_EXIT_MESSAGE}')

            LOGGER.info(error_message)
            sys.exit(1)

    return decorated_func


def get_proxy_from_env(proxy: str) -> Optional[str]:
    return os.getenv(proxy) or os.getenv(proxy.upper())


def parse_error(error_message: str) -> str:
    for pretty_message, pattern in DOCKER_ERROR_PATTERNS.items():
        compiled = re.compile(pattern)
        if re.search(compiled, error_message):
            return pretty_message
    return 'Unexpected Error'
