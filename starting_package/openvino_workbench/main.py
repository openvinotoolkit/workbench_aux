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
from openvino_workbench.arguments_parser import parse_arguments
from openvino_workbench.constants import LOGGER, LOG_FILE
from openvino_workbench.container import Container
from openvino_workbench.docker_config_creator import create_config_for_container
from openvino_workbench.image import Image
from openvino_workbench.utils import print_starting_message, initialize_docker_client, save_logs_on_failure


@save_logs_on_failure
def main():
    # Parse args
    args = parse_arguments()

    # Initialize Docker client
    docker_client: DockerClient = initialize_docker_client(LOGGER)

    # Restart container if needed
    if args.restart:
        container = Container(docker_client=docker_client, logger=LOGGER, config={'name': args.restart})
        # Safe-restart a container, stop it on CMD/Ctrl+C as usual Docker container
        try:
            container.restart(args.detached)
        except KeyboardInterrupt:
            LOGGER.info('Stopping the previously restarted container.')
            container.stop()
            sys.exit(0)

    # Create config for Docker container
    config = create_config_for_container(args, LOGGER)

    # Print starting message
    enabled_devices = {
        'GPU': args.enable_gpu,
        'MYRIAD': args.enable_myriad,
        'HDDL': args.enable_hddl
    }
    print_starting_message(config, enabled_devices, LOG_FILE)

    # Provide proxies for image pulling
    proxies = {}
    if args.http_proxy:
        proxies['http'] = args.http_proxy
    if args.https_proxy:
        proxies['https'] = args.https_proxy
    if args.no_proxy:
        proxies['no_proxy'] = args.no_proxy

    # Safe-pull an image, if interrupted stop pulling with understandable message
    try:
        image = Image(docker_client=docker_client, image_name=args.image, logger=LOGGER, proxies=proxies)
        image.pull(args.force_pull)
    except KeyboardInterrupt:
        LOGGER.info('Image pulling was interrupted.')
        print('Image pulling was interrupted.')
        sys.exit(1)

    # Safe-start a container, stop it on CMD/Ctrl+C as usual Docker container
    container = Container(docker_client=docker_client, logger=LOGGER, config=config)
    try:
        container.start(args.detached, args.network_name, args.network_alias)
    except KeyboardInterrupt:
        container.stop()
        sys.exit(0)


if __name__ == '__main__':
    main()
