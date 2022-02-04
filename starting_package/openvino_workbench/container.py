"""
 OpenVINO DL Workbench Python Starter
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

import logging
import platform
import random
import re
import sys
import time
from typing import Optional

from docker import DockerClient
from openvino_workbench.constants import DL_WB_LOGO, PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES, \
    WORKBENCH_READY_MESSAGE, LOG_FILE, EXAMPLE_COMMAND, INTERNAL_PORT, ABORTING_EXIT_MESSAGE


class Container:
    def __init__(self, docker_client: DockerClient, logger: logging.Logger, config: dict):
        self._client = docker_client
        self._logger = logger
        self.config = config
        self.container_name = self.config['name']
        self._is_present = self._is_container_present()
        self._is_running = self._is_container_running()

    def start(self, detached: bool, network_name: str, network_alias: str):
        self._logger.info('Starting container.')

        if self._is_present:
            print(f'''Container with the specified name "{self.container_name}" is present on the machine.
Use a different name by specifying the `--container-name` argument.
''')

            new_name = self._generate_container_name()
            new_port = self._generate_container_port()
            if new_name:
                message = (f'Copy and run the following command:'
                           f'\n\n\topenvino-workbench --container-name {new_name}')
                if new_port:
                    message += f' --port {new_port}'
                print(f'{message}\n')
            else:
                print(f'Example command: '
                      f'\n\n\topenvino-workbench --container-name NEW_NAME '
                      f'\n\nSubstitute the "NEW_NAME" placeholder with an actual name of your choice.')

            print(ABORTING_EXIT_MESSAGE)
            sys.exit(1)

        print('Starting the DL Workbench container...\n')

        self._client.containers.run(**self.config)

        for pre_message, complete_message in zip(PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES):
            self._wait_for_stage_to_complete(pre_message, re.compile(complete_message))

        self._print_finishing_message(detached)

        # Check for DL WB Docker network and create one if it does not exist
        if 'CLOUD_SERVICE_URL' not in self.config['environment']:
            self._connect_container_to_network(network_name, network_alias)

        self._set_running()

        if not detached:
            # Display container logs
            self._attach_to_container_and_display_logs()

        self._logger.info('Started container in the detached mode.')

    def stop(self):
        self._logger.info('Stopping the container...')
        print('\nStopping the container...')
        if not self._client.containers.list(filters={'name': self.container_name}):
            print('The specified container does not exist.')
            sys.exit(1)
        self._client.api.stop(self.container_name)
        print(f'The container was stopped. Full log of this run can be found in: {LOG_FILE}')
        self._logger.info('The container was stopped.')

    def restart(self, is_detached: bool):
        self._logger.info('Restarting a container.')
        print(f'Restarting a previously stopped container with the name "{self.container_name}" ... \n')
        if not self._is_present:
            self._logger.info('RESTART. Container with specified name was not found.')
            print(f'ERROR: A container with the name "{self.container_name}" does not exist.')
            print(EXAMPLE_COMMAND)
            sys.exit(1)
        elif self._is_running:
            self._logger.info('RESTART. Container with specified name is already running.')
            public_port = self._get_public_port()
            print(f'ERROR: A container with the name "{self.container_name}" is running - there is no need to restart '
                  'it.\n'
                  f'Open the browser and navigate to the http://127.0.0.1:{public_port}')
            sys.exit(1)

        # Get and restart the container
        container = self._client.containers.get(self.container_name)
        container.start()

        # Wait for it to be ready
        for pre_message, complete_message in zip(PRE_STAGE_MESSAGES, STAGE_COMPLETE_MESSAGES):
            self._wait_for_stage_to_complete(pre_message, re.compile(complete_message))

        self._print_finishing_message(is_detached)

        if is_detached:
            sys.exit(0)

        self._set_running()
        self._attach_to_container_and_display_logs()

    def _get_public_port(self) -> Optional[str]:
        bound_ports = self._client.api.port(self.container_name, INTERNAL_PORT)
        if bound_ports:
            return bound_ports[0].get('HostPort')

    def _generate_container_name(self) -> Optional[str]:
        all_taken_names = [container.name for container in self._client.containers.list(all=True)]
        for idx in range(20):
            new_name = f'{self.container_name}_{idx}'
            if new_name not in all_taken_names:
                return new_name

    def _generate_container_port(self) -> Optional[int]:
        taken_port = int(self._get_public_port())
        for _ in range(50):
            new_port = random.randint(5001, 5999)
            if new_port != taken_port:
                return new_port

    def _is_container_present(self) -> bool:
        return any(self.container_name == container.name for container in self._client.containers.list(all=True))

    def _is_container_running(self) -> bool:
        return any(self.container_name == container.name for container in self._client.containers.list())

    def _wait_for_stage_to_complete(self, pre_message: str,
                                    stage_complete_pattern):
        max_retries = 20

        print(pre_message, end=' ', flush=True)

        for _ in range(max_retries):
            time.sleep(7)
            current_log = self._get_docker_logs_since(seconds=20)

            if stage_complete_pattern.search(current_log):
                break
        else:
            self._logger.info('Could not start the container.')
            logs = self._client.api.logs(container=self.container_name).decode('utf-8')
            print(f'\nERROR: Could not start the container. '
                  f'{EXAMPLE_COMMAND}'
                  f'{ABORTING_EXIT_MESSAGE}')
            self._logger.info(f'CONTAINER LOGS\n: {logs}.')
            sys.exit(1)

        self._logger.info(f'Container starting stage with message {stage_complete_pattern.pattern} is complete.')

        print('Done.')

    def _print_finishing_message(self, detached: bool):
        print(DL_WB_LOGO)

        # Show finishing message from the container logs
        container = self._client.containers.get(self.container_name)
        all_logs = container.logs().decode('utf-8').rstrip()
        finishing_message_start = all_logs.rfind(WORKBENCH_READY_MESSAGE)
        print(f'\n{all_logs[finishing_message_start:]}')
        del all_logs

        if detached:
            print(f'''\nDL Workbench is started in the detached mode.
            If you want to stop the container, run the following command:
                    docker stop {self.container_name}''')
        else:
            stop_message = '\nPress Ctrl+C to stop the container.'
            if platform.system() == 'Darwin':
                stop_message = stop_message.replace('Ctrl', 'CMD')
            print(stop_message)

        self._logger.info('Finish message was printed.')

    def _is_network_present(self, network: str) -> bool:
        return bool(self._client.api.networks(names=[network]))

    def _connect_container_to_network(self,
                                      network_name: str,
                                      network_alias: str):
        if not self._is_network_present(network_name):
            net = self._client.networks.create(name=network_name, driver='bridge')
        else:
            net_id = self._client.api.networks(names=[network_name])[0]['Id']
            net = self._client.networks.get(network_id=net_id)

        net.connect(container=self.container_name, aliases=[network_alias])

    def _get_docker_logs_since(self, seconds: int) -> str:
        return self._client.api.logs(container=self.container_name,
                                     since=int(time.time()) - seconds).decode('utf-8')

    def _attach_to_container_and_display_logs(self):
        self._logger.info('Attaching to the container to display logs.')
        for log in self._client.api.attach(container=self.container_name, stream=True):
            print(log.decode('utf-8'), sep='', end='')

    def _set_present(self):
        self._is_present = True

    def _set_running(self):
        self._is_present = True
        self._is_running = True
