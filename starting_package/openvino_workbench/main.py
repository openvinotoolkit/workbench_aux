"""
 OpenVINO Profiler
 Entrypoint for the DL Workbench Python starter wrapper

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

from openvino_workbench.arguments_parser import parse_arguments
from openvino_workbench.container import start_container, stop_container
from openvino_workbench.docker_config_creator import create_config_for_container
from openvino_workbench.image import pull_image_and_display_progress
from openvino_workbench.utils import print_starting_message, initialize_docker_client

from docker import DockerClient


def main():
    # Parse args
    args = parse_arguments()

    # Initialize Docker client
    docker_client: DockerClient = initialize_docker_client()

    # Create config for Docker container
    config = create_config_for_container(args)

    # Print starting message
    enabled_devices = {
        'GPU': args.enable_gpu,
        'MYRIAD': args.enable_myriad,
        'HDDL': args.enable_hddl
    }
    print_starting_message(config, enabled_devices)

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

        pull_image_and_display_progress(docker_client, args.image, proxies, args.force_pull)
    except KeyboardInterrupt:
        print('Image pulling was interrupted.')
        sys.exit(1)

    # Safe-start a container, stop it on CMD/Ctrl+C as usual Docker container
    try:
        start_container(docker_client, config, args.network_name, args.network_alias, args.detached)
    except KeyboardInterrupt:
        stop_container(docker_client, config['name'])
        sys.exit(0)


if __name__ == '__main__':
    main()
