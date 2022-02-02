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
import pathlib
import platform
import sys
import time
import traceback
import tempfile
from typing import Dict, Union

import requests

import docker

from openvino_workbench.constants import INTERNAL_PORT, COMMUNITY_LINK


def print_starting_message(config: dict, enabled_devices: dict):
    bound_ip, port = config['ports'][INTERNAL_PORT]
    print('\nStarting the DL Workbench with the following arguments:\n'
          f'Image Name: {config["image"]}\n'
          f'Container Name: {config["name"]}\n'
          f'IP: {bound_ip}\n'
          f'Port: {port}\n'
          f'GPU Enabled: {"True" if enabled_devices["GPU"] else "False"}\n'
          f'MYRIAD Enabled: {"True" if enabled_devices["MYRIAD"] else "False"}\n'
          f'HDDL Enabled: {"True" if enabled_devices["HDDL"] else "False"}\n')


def initialize_docker_client() -> docker.DockerClient:
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        print('Could not initialize the Docker client from environment.')
        if platform.system() in ('Windows', 'Darwin'):
            print('Please check if the Docker Desktop is running.')
        else:
            print('Please check if the Docker daemon is running.')
        sys.exit(1)
    return client


def create_log_file(prefix: str, suffix: str = '.log') -> Dict[str, Union[str, int]]:
    log_fd, log_path = tempfile.mkstemp(text=True, prefix=prefix, suffix=suffix)
    return {
        'log_path': log_path,
        'log_fd': log_fd
    }


def save_logs_on_failure(docker_client: docker.DockerClient, container_name: str):
    def decorator(fnc):
        def decorated_func(*args, **kwargs):
            try:
                return fnc(*args, **kwargs)
            except Exception as error:

                # Write Python logs
                error_message = str(error)
                error_type = type(error)
                error_traceback = traceback.format_exc()
                starter_log_file = create_log_file('openvino_workbench_')

                with open(starter_log_file['log_fd'], mode='w', encoding='utf-8') as log_file:
                    log = f'''\nOpenVINO Workbench Python Starter Error Log:
                    * An error occurred!
                    * Error Message: {error_message if error_message else None}
                    * Error Type: {error_type}
                    
                    * The complete log is saved at {starter_log_file["log_path"]}.'''
                    print(log)
                    log += f'\n * Complete traceback: {error_traceback}'
                    log_file.write(log)

                # Write container logs
                if is_container_present(docker_client, container_name):
                    container_log_file = create_log_file('openvino_workbench_container_')
                    container_logs = docker_client.api.logs(container=container_name)
                    with open(container_log_file['log_fd'], mode='w', encoding='utf-8') as log_file:
                        log = f'Container logs: \n{container_logs}'
                        log_file.write(log)
                    print(
                        f'The complete container log is saved at {container_log_file["log_path"]}.')
                print(f'Please report the logs to the: {COMMUNITY_LINK}.')
                sys.exit(1)

        return decorated_func
    return decorator
