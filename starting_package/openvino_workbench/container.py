"""
 OpenVINO Profiler
 Docker container-related logic

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

import platform
import re
import sys
import time

from docker import DockerClient

from openvino_workbench.constants import DL_WB_LOGO, PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES, \
    WORKBENCH_READY_MESSAGE
from openvino_workbench.utils import get_docker_logs_since


def wait_for_stage_to_complete(pre_message: str,
                               stage_complete_pattern,
                               docker_client: DockerClient,
                               container_name: str):
    max_retries = 20

    print(pre_message, end=' ', flush=True)

    for _ in range(max_retries):
        time.sleep(7)
        current_log = get_docker_logs_since(docker_client=docker_client,
                                            container_name=container_name,
                                            seconds=20)

        if stage_complete_pattern.search(current_log):
            break
    else:
        print(docker_client.api.logs(container=container_name).decode('utf-8'))
        print('\nCould not start the container. The complete log is shown above.')
        sys.exit(1)

    print('Done.')


def print_finishing_message(docker_client: DockerClient, container_name: str, is_detached: bool):
    print(DL_WB_LOGO)

    # Show finishing message from the container logs
    container = docker_client.containers.get(container_name)
    all_logs = container.logs().decode('utf-8').rstrip()
    finishing_message_start = all_logs.rfind(WORKBENCH_READY_MESSAGE)
    print(f'\n{all_logs[finishing_message_start:]}')
    del all_logs

    if is_detached:
        print(f'''\nDL Workbench is started in the detached mode.
        If you want to stop the container, run the following command:
                docker stop {container_name}''')
    else:
        stop_message = '\nPress Ctrl+C to stop the container.'
        if platform.system() == 'Darwin':
            stop_message = stop_message.replace('Ctrl', 'CMD')
        print(stop_message)


def is_network_present(docker_client: DockerClient, network: str) -> bool:
    return bool(docker_client.api.networks(names=[network]))


def connect_container_to_network(docker_client: DockerClient,
                                 container_name: str,
                                 network_name: str,
                                 network_alias: str):
    if not is_network_present(docker_client, network_name):
        net = docker_client.networks.create(name=network_name, driver='bridge')
    else:
        net_id = docker_client.api.networks(names=[network_name])[0]['Id']
        net = docker_client.networks.get(network_id=net_id)

    net.connect(container=container_name, aliases=[network_alias])


def is_container_present(docker_client: DockerClient, container_name_to_search: str) -> bool:
    return any(container_name_to_search == container.name for container in docker_client.containers.list(all=True))


def is_container_running(docker_client: DockerClient, container_name_to_search: str) -> bool:
    return any(container_name_to_search == container.name for container in docker_client.containers.list())


def start_container(docker_client: DockerClient,
                    config: dict,
                    network: str,
                    network_alias: str,
                    detached: bool = False):
    if is_container_present(docker_client, config['name']):
        print(f'Container with specified name "{config["name"]}" is present on the machine.'
              '\nUse different name by specifying `--container-name` argument.'
              '\nAborting.')
        sys.exit(1)

    print('Starting the DL Workbench container...\n')

    docker_client.containers.run(**config)

    for pre_message, complete_message in zip(PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES):
        wait_for_stage_to_complete(pre_message, re.compile(complete_message), docker_client, config['name'])

    print_finishing_message(docker_client, config['name'], detached)

    # Check for DL WB Docker network and create one if it does not exist
    if 'CLOUD_SERVICE_URL' not in config['environment']:
        connect_container_to_network(docker_client, config['name'], network, network_alias)

    if not detached:
        # Display container logs
        attach_to_container_and_display_logs(docker_client, config['name'])


def stop_container(docker_client: DockerClient, container_name: str):
    print('\nStopping the container...')
    if not docker_client.containers.list(filters={'name': container_name}):
        print('The specified container does not exist.')
        sys.exit(1)
    docker_client.api.stop(container_name)
    print('The container was stopped.')


def restart_container(docker_client: DockerClient, container_name: str, is_detached: bool):
    print(f'Restarting a previously stopped container with the name "{container_name}" ... \n')
    if not is_container_present(docker_client, container_name):
        print(f'A container with the name "{container_name}" does not exist.')
        print('Aborting.')
        sys.exit(1)
    elif is_container_running(docker_client, container_name):
        print(f'A container with the name "{container_name}" is running - there is no need to restart it.')
        print('Aborting.')
        sys.exit(1)

    # Get and restart the container
    container = docker_client.containers.get(container_name)
    container.start()

    # Wait for it to be ready
    for pre_message, complete_message in zip(PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES):
        wait_for_stage_to_complete(pre_message, re.compile(complete_message), docker_client, container_name)

    print_finishing_message(docker_client, container_name, is_detached)

    if is_detached:
        sys.exit(0)

    attach_to_container_and_display_logs(docker_client, container_name)


def attach_to_container_and_display_logs(docker_client: DockerClient, container_name: str):
    for log in docker_client.api.attach(container=container_name, stream=True):
        print(log.decode('utf-8'), sep='', end='')
