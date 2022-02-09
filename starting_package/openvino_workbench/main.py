"""
 OpenVINO DL Workbench Python Starter
 Entrypoint for the DL Workbench Python Starter

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
import sys

from docker import DockerClient
from openvino_workbench.arguments_parser import StarterArgumentsParser
from openvino_workbench.constants import LOGGER, LOG_FILE, ABORTING_EXIT_MESSAGE
from openvino_workbench.container import DockerContainer
from openvino_workbench.docker_config_creator import DockerConfigCreator
from openvino_workbench.image import DockerImage
from openvino_workbench.utils import print_starting_message, initialize_docker_client, save_logs_on_failure


@save_logs_on_failure
def main():
    # Parse arguments
    arguments = StarterArgumentsParser().arguments

    # Initialize Docker client
    docker_client: DockerClient = initialize_docker_client()

    # Restart container if needed
    if arguments.restart:
        container = DockerContainer(docker_client=docker_client, config={'name': arguments.restart})
        # Safe-restart a container, stop it on CMD/Ctrl+C as usual Docker container
        try:
            container.restart(arguments.detached)
        except KeyboardInterrupt:
            LOGGER.debug('Stopping the previously restarted container.')
            container.stop()
            sys.exit(0)

    # Create config for Docker container
    # config = create_config_for_container(arguments, LOGGER)
    config = DockerConfigCreator(arguments=arguments).config

    # Print starting message
    enabled_devices = {
        'GPU': arguments.enable_gpu,
        'MYRIAD': arguments.enable_myriad,
        'HDDL': arguments.enable_hddl
    }
    print_starting_message(config=config, enabled_devices=enabled_devices, log_file=LOG_FILE)

    # Provide proxies for image pulling
    proxies = {}
    if arguments.http_proxy:
        proxies['http'] = arguments.http_proxy
    if arguments.https_proxy:
        proxies['https'] = arguments.https_proxy
    if arguments.no_proxy:
        proxies['no_proxy'] = arguments.no_proxy

    # Safe-pull an image, if interrupted stop pulling with understandable message
    try:
        image = DockerImage(docker_client=docker_client, image_name=arguments.image, proxies=proxies)
        image.pull(arguments.force_pull)
    except KeyboardInterrupt:
        LOGGER.debug('Image pulling was interrupted.')
        LOGGER.info('Image pulling was interrupted. \n%s', ABORTING_EXIT_MESSAGE)
        sys.exit(1)

    # Safe-start a container, stop it on CMD/Ctrl+C as usual Docker container
    container = DockerContainer(docker_client=docker_client, config=config)
    try:
        container.start(detached=arguments.detached,
                        network_name=arguments.network_name,
                        network_alias=arguments.network_alias)
    except KeyboardInterrupt:
        container.stop()
        sys.exit(0)


if __name__ == '__main__':
    main()
