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

from openvino_workbench.constants import DL_WB_LOGO, PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES
from openvino_workbench.utils import get_tokens_from_logs, get_docker_logs_since

from docker import DockerClient


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


def print_finish_message(protocol: str, port: int, tokens: dict):
    link = f'{protocol}://127.0.0.1:{port}/'
    message = f'DL Workbench is available at {link}'

    print(DL_WB_LOGO)

    if 'login_token' not in tokens or 'url_token' not in tokens:
        print(message)
        return

    print(f'{message}?token={tokens["url_token"]}\n'
          '\nNote: Authentication with the token inside this link is available only once.\n'
          f'The link expires after you click it. Use your login token at {link} to '
          'authenticate again.\n')

    print(f'Login token: {tokens["login_token"]}\n')

    print(f'Note: Use this token to authenticate at {link} \n'
          'The login token is saved inside the Docker container.\n')

    print(f'Token for Jupyter Lab: {tokens["login_token"]}')


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


def start_container(docker_client: DockerClient,
                    config: dict,
                    network: str,
                    network_alias: str,
                    detached: bool = False):
    if docker_client.containers.list(filters={'name': config['name']}, all=True):
        print(f'Container with specified name "{config["name"]}" is present on the machine.'
              '\nUse different name by specifying `--container-name` argument.'
              '\nAborting.')
        sys.exit(1)

    print('Starting DL Workbench container...\n')

    docker_client.containers.run(**config)

    for pre_message, complete_message in zip(PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES):
        wait_for_stage_to_complete(pre_message, re.compile(complete_message), docker_client, config['name'])

    tokens = {}
    if 'ENABLE_AUTH' in config['environment']:
        tokens = get_tokens_from_logs(docker_client=docker_client, container_name=config['name'])

    protocol = 'https' if 'SSL_KEY' in config['environment'] else 'http'
    print_finish_message(protocol=protocol, port=config['ports']['5665'], tokens=tokens)

    # Check for DL WB Docker network and create one if it does not exist
    connect_container_to_network(docker_client, config['name'], network, network_alias)

    if not detached:
        finishing_message = '\nPress Ctrl+C to stop the container.'
        if platform.system() == 'Darwin':
            finishing_message = finishing_message.replace('Ctrl', 'CMD')
        print(finishing_message)

        # Display container logs
        for log in docker_client.api.attach(container=config['name'], stream=True):
            print(log.decode('utf-8'), sep='', end='')
    else:
        print(f'''\nDL Workbench is started in detached mode.
If you want to stop the container, run the following command:
        docker stop {config["name"]}''')


def stop_container(docker_client: DockerClient, container_name: str):
    print('\nStopping container...')
    if not docker_client.containers.list(filters={'name': container_name}):
        print('The specified container does not exist.')
        sys.exit(1)
    docker_client.api.stop(container_name)
    print('Container was stopped.')
