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
from typing import Optional


def get_proxy_from_env(proxy: str) -> Optional[str]:
    return os.getenv(proxy) or os.getenv(proxy.upper())


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='DL Workbench is an official UI environment of the OpenVINO™ toolkit.')

    parser.add_argument('--image',
                        required=False,
                        help='Specifies the DL Workbench Docker image name.',
                        default='openvino/workbench:2021.4')

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

    if not args.assets_directory and (args.ssl_key_name or args.ssl_certificate_name):
        parser.error('"--assets-directory" is required for SSL. SSL key and certificate should be placed there.')
    if (not args.ssl_key_name and args.ssl_certificate_name) or (args.ssl_key_name and not args.ssl_certificate_name):
        parser.error('Both SSL certificate name and SSL key name are required.')

    return args
