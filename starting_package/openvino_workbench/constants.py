"""
 OpenVINO Profiler
 Constant variables

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
import os
import tempfile

CLI_COMMAND = 'openvino-workbench'

DOCKER_HUB_TAGS_URL = 'https://hub.docker.com/v2/repositories/openvino/workbench/tags'

STARTED_DB_MESSAGE = 'PostgreSQL ready for start up'
STARTED_NGINX_MESSAGE = 'Starting nginx nginx'
STARTED_CELERY_MESSAGE = r'(Celery ready for start up|1 node online)'
WORKBENCH_READY_MESSAGE = 'DL Workbench is available at'

STAGE_COMPLETE_MESSAGES = (STARTED_DB_MESSAGE, STARTED_NGINX_MESSAGE, STARTED_CELERY_MESSAGE, WORKBENCH_READY_MESSAGE)

PRE_STAGE_MESSAGES = ('Starting Database...', 'Starting Nginx...', 'Starting Celery...', 'Finishing up...')

DL_WB_LOGO = r'''
    ____  __       _       __           __   __                    __  
   / __ \/ /      | |     / /___  _____/ /__/ /_  ___  ____  _____/ /_ 
  / / / / /       | | /| / / __ \/ ___/ //_/ __ \/ _ \/ __ \/ ___/ __ \
 / /_/ / /___     | |/ |/ / /_/ / /  / ,< / /_/ /  __/ / / / /__/ / / /
/_____/_____/     |__/|__/\____/_/  /_/|_/_.___/\___/_/ /_/\___/_/ /_/ 
'''

EXAMPLE_COMMAND = '\nCopy and run the following command to start the highest available version of DL Workbench: ' \
                  f'\n\n\t{CLI_COMMAND} --image openvino/workbench:latest --force-pull\n'

DL_WB_DOCKER_CONFIG_PATH = os.path.join('/home', 'workbench', '.workbench')

INTERNAL_PORT = '5665'

COMMUNITY_LINK = 'https://community.intel.com/t5/Intel-Distribution-of-OpenVINO/bd-p/distribution-openvino-toolkit'

DOCKER_ERROR_PATTERNS = {'Port is already allocated. Specify a different port using the "--port" argument':
                             r'port\sis\salready\sallocat'}

# Initialize logger
_, LOG_FILE = tempfile.mkstemp(text=True, prefix='openvino_workbench_', suffix='.log')
LOGGER_NAME = 'Python Starter Logger'
LOGGER = logging.getLogger(LOGGER_NAME)

# Handler for the info visible to a user
user_info_handler = logging.StreamHandler()
user_info_formatter = logging.Formatter('%(message)s')
user_info_handler.setFormatter(user_info_formatter)
user_info_handler.setLevel(logging.INFO)
LOGGER.addHandler(user_info_handler)

# Handler for the debug information sent to the LOG_FILE
debug_handler = logging.FileHandler(filename=LOG_FILE, mode='a')
debug_handler_formatter = logging.Formatter('[%(levelname)s] %(message)s (%(filename)s, %(funcName)s(), line %('
                                            'lineno)d)')
debug_handler.setFormatter(debug_handler_formatter)
debug_handler.setLevel(logging.DEBUG)
LOGGER.addHandler(debug_handler)

LOGGER.setLevel(logging.DEBUG)
LOGGER.debug('OpenVINO Python Starter Log')

ABORTING_EXIT_MESSAGE = (f'\nComplete log can be found in: {LOG_FILE}'
                         f'\nPlease report this log to: {COMMUNITY_LINK}'
                         '\n\nAborting.\n')
