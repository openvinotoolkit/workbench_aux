"""
 OpenVINO DL Workbench Python Starter
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
import sys
import logging
import platform
from openvino_workbench.constants import EXAMPLE_COMMAND, ABORTING_EXIT_MESSAGE
from openvino_workbench.utils import get_proxy_from_env


class StarterArgumentsParser:
    def __init__(self, logger: logging.Logger):
        self._logger = logger
        self._logger.info('Parsing arguments.')

        self._parser = argparse.ArgumentParser(description='DL Workbench is an official UI environment of the '
                                                           'OpenVINO™ toolkit.')
        self._add_arguments_to_parser()
        self.arguments = self._parser.parse_args()
        self._validate_arguments()

    def _add_arguments_to_parser(self):
        self._parser.add_argument('--image',
                                  required=False,
                                  help='Specifies the DL Workbench Docker image name.',
                                  default='openvino/workbench:2021.4.2')

        self._parser.add_argument('--force-pull',
                                  action='store_true',
                                  required=False,
                                  help='Force-pull the specified image. Can be used to download a '
                                       'newer version of the DL Workbench image.',
                                  default=False)

        self._parser.add_argument('--ip',
                                  required=False,
                                  help='Specifies the outside IP on which DL Workbench will be available.',
                                  default='0.0.0.0')  # nosec

        self._parser.add_argument('--port',
                                  required=False,
                                  type=int,
                                  help='Maps the Docker container port to the provided host port '
                                       'to get access to the DL Workbench from a web browser.',
                                  default=5665)

        self._parser.add_argument('--container-name',
                                  required=False,
                                  help='Specifies the DL Workbench container name to use.',
                                  default='workbench')

        self._parser.add_argument('--detached',
                                  action='store_true',
                                  required=False,
                                  help='Enables the detached mode of the Docker container.'
                                       'Container logs will not be visible in the terminal.',
                                  default=False)

        self._parser.add_argument('--restart',
                                  required=False,
                                  help='Restarts a previously stopped DL Workbench container. '
                                       'Provide the container name to restart. '
                                       'If specified, other arguments are not supported. DL Workbench will have the '
                                       'capabilities '
                                       'that were enabled on the first run.')

        # Devices
        self._parser.add_argument('--enable-gpu',
                                  action='store_true',
                                  required=False,
                                  help='Enables the DL Workbench container to use GPU devices '
                                       'by providing Docker container with GPU-related arguments.',
                                  default=False)

        hddl_vpu = self._parser.add_mutually_exclusive_group()
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
        self._parser.add_argument('--assets-directory',
                                  required=False,
                                  help='Mounts a provided local directory to the "/home/workbench/.workbench" '
                                       'directory in the Docker container. '
                                       'The directory is not mounted by default. Format: /path/to/directory')

        # Proxies
        self._parser.add_argument('--http-proxy',
                                  required=False,
                                  help='Specifies the HTTP proxy to use in the DL Workbench container.',
                                  default=get_proxy_from_env('http_proxy'))

        self._parser.add_argument('--https-proxy',
                                  required=False,
                                  help='Specifies the HTTPS proxy to use in the DL Workbench container.',
                                  default=get_proxy_from_env('https_proxy'))

        self._parser.add_argument('--no-proxy',
                                  required=False,
                                  help='Specifies URLs to be excluded from proxying. Format: "url1,url2,url3".',
                                  default=get_proxy_from_env('no_proxy'))

        # Capabilities
        self._parser.add_argument('--no-jupyter',
                                  action='store_true',
                                  required=False,
                                  help='The Jupyter server will not be started inside the DL Workbench container.',
                                  default=False)

        self._parser.add_argument('--enable-authentication',
                                  action='store_true',
                                  required=False,
                                  help='Turns on authentication for the DL Workbench.',
                                  default=False)

        # SSL
        self._parser.add_argument('--ssl-certificate-name',
                                  required=False,
                                  help='Specifies the name of the SSL certificate file. '
                                       'The file should be placed in the directory provided in the "assets-directory" '
                                       'argument. '
                                       'Example: certificate.pem')
        self._parser.add_argument('--ssl-key-name',
                                  required=False,
                                  help='Specifies the name of the SSL key file. '
                                       'The file should be placed in the directory provided in the "assets-directory" '
                                       'argument. '
                                       'Example: key.pem')
        self._parser.add_argument('--verify-ssl',
                                  action='store_true',
                                  required=False,
                                  help='Sets the TLS certificate as trusted (\'on\').',
                                  default=True)

        # DevCloud
        self._parser.add_argument('--cloud-service-address',
                                  required=False,
                                  help='Specifies the URL to a standalone cloud service '
                                       'that provides Intel(R) hardware capabilities for experiments.')
        self._parser.add_argument('--cloud-service-session-ttl',
                                  required=False,
                                  help='Specifies the cloud service session time to live in minutes.')

        # Network
        self._parser.add_argument('--network-name',
                                  required=False,
                                  help='Specifies the name of a Docker network to run the Docker container in.',
                                  default='workbench_network')
        self._parser.add_argument('--network-alias',
                                  required=False,
                                  help='Specifies the alias of the DL Workbench container in the network.',
                                  default='workbench')

        # Misc
        self._parser.add_argument('--base-prefix',
                                  required=False,
                                  help='Specifies the base prefix of the DL Workbench web application.',
                                  default='/')

    def _validate_arguments(self):
        self._validate_restart_arguments()
        self._validate_ssl_arguments()
        if platform.system() == 'Windows':
            self._validate_arguments_for_windows()

    def _validate_ssl_arguments(self):
        self._logger.info('Validating arguments for SSL.')
        # Check for SSL-related files
        if not self.arguments.assets_directory and (self.arguments.ssl_key_name or self.arguments.ssl_certificate_name):
            self._logger.info('SSL key and/or certificate were provided without the assets directory.')
            self._parser.error('ERROR: "--assets-directory" is required for SSL. SSL key and certificate should be '
                               'placed there.'
                               '\nExample command:'
                               '\n\n\topenvino-workbench --assets-directory /path/to/assets --ssl-key-name key.pem '
                               '--ssl-certificate-name certificate.pem'
                               f'{ABORTING_EXIT_MESSAGE}')
        if (not self.arguments.ssl_key_name and self.arguments.ssl_certificate_name) or (
                self.arguments.ssl_key_name and not self.arguments.ssl_certificate_name):
            self._logger.info('Only one of the SSL files was provided.')
            self._parser.error('ERROR: Both SSL certificate name and SSL key name are required.'
                               '\nExample command:'
                               '\n\n\t openvino-workbench --assets-directory /path/to/assets --ssl-key-name key.pem '
                               '--ssl-certificate-name certificate.pem'
                               f'{ABORTING_EXIT_MESSAGE}')

    def _validate_restart_arguments(self):
        if not self.arguments.restart:
            return
        self._logger.info('Validating arguments for restart.')
        # If detached restart is needed then there should be exactly 4 arguments
        # and '--detached' should be one of them
        if self.arguments.detached and len(sys.argv) != 4:
            self._logger.info('Error with restarting in the detached mode. Incorrect number of arguments. '
                              f'{vars(self.arguments)}')
            self._parser.error(
                'ERROR: Unrecognized arguments for restart. '
                'To restart the container in the detached mode, '
                'provide the "--detached" argument and the container name following the "--restart" argument. '
                'The only other argument available with "--restart" is "--detached".'
                '\nExample command: '
                f'\n\n\topenvino-workbench --restart {self.arguments.restart} --detached'
                f'{ABORTING_EXIT_MESSAGE}')
        # If regular restart is needed then there should be exactly 3 arguments
        elif not self.arguments.detached and len(sys.argv) != 3:
            self._logger.info('Error with restarting in the interactive mode. Incorrect number of arguments. '
                              f'{vars(self.arguments)}')
            self._parser.error(
                'ERROR: Unrecognized arguments for restart. '
                'To restart the container, provide the container name following the "--restart" argument. '
                'The only other argument available with "--restart" is "--detached".'
                '\nExample command: '
                '\n\n\topenvino-workbench --restart workbench'
                f'{ABORTING_EXIT_MESSAGE}')

    def _validate_arguments_for_windows(self):
        any_device_enabled = any((self.arguments.enable_myriad, self.arguments.enable_hddl, self.arguments.enable_gpu))
        if any_device_enabled:
            self._logger.info('Additional device(s) are enabled for Windows. '
                              f'{vars(self.arguments)}')
            self._parser.error(
                'ERROR: DL Workbench does not support non-CPU (GPU, VPU, HDDL) devices on Windows.\n'
                'Please remove the non-CPU related arguments (--enable-gpu/--enable-myriad/--enable-hddl) and try '
                'again.'
                f'{EXAMPLE_COMMAND}'
                f'{ABORTING_EXIT_MESSAGE}')
