"""
 OpenVINO Profiler
 Arguments parser for the DL Workbench Python Starter

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

import argparse
import os
import sys
from typing import Optional


def get_proxy_from_env(proxy: str) -> Optional[str]:
    return os.getenv(proxy) or os.getenv(proxy.upper())


def validate_args_for_restart(args: argparse.Namespace, parser: argparse.ArgumentParser):
    # If detached restart is needed then there should be exactly 4 arguments
    # and '--detached' should be one of them
    if args.detached and len(sys.argv) != 4:
        parser.error(
            'Unrecognized arguments for restart. '
            'To restart the container in the detached mode, '
            'provide the "--detached" argument and the container name following the "--restart" argument. '
            'The only other argument available with "--restart" is "--detached".\n'
            'Example: openvino-workbench --restart workbench --detached')
    # If regular restart is needed then there should be exactly 3 arguments
    elif not args.detached and len(sys.argv) != 3:
        parser.error(
            'Unrecognized arguments for restart. '
            'To restart the container, provide the container name following the "--restart" argument. '
            'The only other argument available with "--restart" is "--detached".\n'
            'Example: openvino-workbench --restart workbench')


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='DL Workbench is an official UI environment of the OpenVINO™ toolkit.')

    parser.add_argument('--image',
                        required=False,
                        help='Specifies the DL Workbench Docker image name.',
                        default='openvino/workbench:2021.4.1')

    parser.add_argument('--force-pull',
                        action='store_true',
                        required=False,
                        help='Force-pull the specified image. Can be used to download a '
                             'newer version of the DL Workbench image.',
                        default=False)

    parser.add_argument('--ip',
                        required=False,
                        help='Specifies the outside IP on which DL Workbench will be available.',
                        default='0.0.0.0')  # nosec

    parser.add_argument('--port',
                        required=False,
                        type=int,
                        help='Maps the Docker container port to the provided host port '
                             'to get access to the DL Workbench from a web browser.',
                        default=5665)

    parser.add_argument('--container-name',
                        required=False,
                        help='Specifies the DL Workbench container name to use.',
                        default='workbench')

    parser.add_argument('--detached',
                        action='store_true',
                        required=False,
                        help='Enables the detached mode of the Docker container.'
                             'Container logs will not be visible in the terminal.',
                        default=False)

    parser.add_argument('--restart',
                        required=False,
                        help='Restarts a previously stopped DL Workbench container. '
                             'Provide the container name to restart. '
                             'If specified, other arguments are not supported. DL Workbench will have the capabilities '
                             'that were enabled on the first run.')

    # Devices
    parser.add_argument('--enable-gpu',
                        action='store_true',
                        required=False,
                        help='Enables the DL Workbench container to use GPU devices '
                             'by providing Docker container with GPU-related arguments.',
                        default=False)

    hddl_vpu = parser.add_mutually_exclusive_group()
    hddl_vpu.add_argument('--enable-myriad',
                          action='store_true',
                          required=False,
                          help='Enables MYRIAD in the DL Workbench container. '
                               'NOTE: MYRIAD and HDDL arguments cannot be set simultaneously.',
                          default=False)
    hddl_vpu.add_argument('--enable-hddl',
                          action='store_true',
                          required=False,
                          help='Enables HDDL in the DL Workbench container. '
                               'NOTE: MYRIAD and HDDL arguments cannot be set simultaneously.',
                          default=False)

    # Assets
    parser.add_argument('--assets-directory',
                        required=False,
                        help='Mounts a provided local directory to the "/home/workbench/.workbench" '
                             'directory in the Docker container. '
                             'The directory is not mounted by default. Format: /path/to/directory')

    # Proxies
    parser.add_argument('--http-proxy',
                        required=False,
                        help='Specifies the HTTP proxy to use in the DL Workbench container.',
                        default=get_proxy_from_env('http_proxy'))

    parser.add_argument('--https-proxy',
                        required=False,
                        help='Specifies the HTTPS proxy to use in the DL Workbench container.',
                        default=get_proxy_from_env('https_proxy'))

    parser.add_argument('--no-proxy',
                        required=False,
                        help='Specifies URLs to be excluded from proxying. Format: "url1,url2,url3".',
                        default=get_proxy_from_env('no_proxy'))

    # Capabilities
    parser.add_argument('--no-jupyter',
                        action='store_true',
                        required=False,
                        help='The Jupyter server will not be started inside the DL Workbench container.',
                        default=False)

    parser.add_argument('--enable-authentication',
                        action='store_true',
                        required=False,
                        help='Turns on authentication for the DL Workbench.',
                        default=False)

    # SSL
    parser.add_argument('--ssl-certificate-name',
                        required=False,
                        help='Specifies the name of the SSL certificate file. '
                             'The file should be placed in the directory provided in the "assets-directory" argument. '
                             'Example: certificate.pem')
    parser.add_argument('--ssl-key-name',
                        required=False,
                        help='Specifies the name of the SSL key file. '
                             'The file should be placed in the directory provided in the "assets-directory" argument. '
                             'Example: key.pem')
    parser.add_argument('--verify-ssl',
                        action='store_true',
                        required=False,
                        help='Sets the TLS certificate as trusted (\'on\').',
                        default=True)

    # DevCloud
    parser.add_argument('--cloud-service-address',
                        required=False,
                        help='Specifies the URL to a standalone cloud service '
                             'that provides Intel(R) hardware capabilities for experiments.')
    parser.add_argument('--cloud-service-session-ttl',
                        required=False,
                        help='Specifies the cloud service session time to live in minutes.')

    # Network
    parser.add_argument('--network-name',
                        required=False,
                        help='Specifies the name of a Docker network to run the Docker container in.',
                        default='workbench_network')
    parser.add_argument('--network-alias',
                        required=False,
                        help='Specifies the alias of the DL Workbench container in the network.',
                        default='workbench')

    # Misc
    parser.add_argument('--base-prefix',
                        required=False,
                        help='Specifies the base prefix of the DL Workbench web application.',
                        default='/')

    args = parser.parse_args()

    # Check if restart is needed
    # There should be exactly 3 OR 4 args:
    # 1: path to the script, 2: '--restart', 3: container name to restart, OPTIONAL 4: '--detached'
    if args.restart:
        validate_args_for_restart(args, parser)

    # Check for SSL-related files
    if not args.assets_directory and (args.ssl_key_name or args.ssl_certificate_name):
        parser.error('"--assets-directory" is required for SSL. SSL key and certificate should be placed there.')
    if (not args.ssl_key_name and args.ssl_certificate_name) or (args.ssl_key_name and not args.ssl_certificate_name):
        parser.error('Both SSL certificate name and SSL key name are required.')

    return args
