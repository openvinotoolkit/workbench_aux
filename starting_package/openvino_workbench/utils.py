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
import platform
import sys
import re
import time

import requests

from openvino_workbench.constants import URL_TOKEN_REGEXP, LOGIN_TOKEN_REGEXP

import docker


def get_image_size(repository_tags_url: str, proxies: dict) -> int:
    try:
        images_info = requests.get(repository_tags_url, proxies=proxies).json()
        return images_info['results'][0]['full_size']
    except Exception:
        return 0


def print_starting_message(config: dict, enabled_devices: dict):
    print('\nStarting the DL Workbench with the following arguments:\n'
          f'Image Name: {config["image"]}\n'
          f'Container Name: {config["name"]}\n'
          f'IP: {config["hostname"]}\n'
          f'Port: {config["ports"]["5665"]}\n'
          f'GPU Enabled: {"True" if enabled_devices["GPU"] else "False"}\n'
          f'MYRIAD Enabled: {"True" if enabled_devices["MYRIAD"] else "False"}\n'
          f'HDDL Enabled: {"True" if enabled_devices["HDDL"] else "False"}\n')


def initialize_docker_client() -> docker.DockerClient:
    try:
        client = docker.from_env()
    except docker.errors.DockerException:
        print('Could not initialize Docker client from environment.')
        if platform.system() in ('Windows', 'Darwin'):
            print('Please check if Docker Desktop is running.')
        else:
            print('Please check if Docker daemon is running.')
        sys.exit(1)
    return client


def get_tokens_from_logs(docker_client: docker.DockerClient, container_name: str) -> dict:
    logs = get_docker_logs_since(docker_client, container_name, seconds=10)

    tokens = dict()

    login_token_groups = re.search(LOGIN_TOKEN_REGEXP, logs)
    if login_token_groups:
        tokens['login_token'] = login_token_groups.group(1)

    url_token_groups = re.search(URL_TOKEN_REGEXP, logs)
    if url_token_groups:
        tokens['url_token'] = url_token_groups.group(1)

    return tokens


def get_docker_logs_since(docker_client: docker.DockerClient, container_name: str, seconds: int) -> str:
    return docker_client.api.logs(container=container_name,
                                  since=int(time.time()) - seconds).decode('utf-8')
