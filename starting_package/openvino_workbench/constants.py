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

import os

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

DL_WB_DOCKER_CONFIG_PATH = os.path.join('/home', 'workbench', '.workbench')

URL_TOKEN_REGEXP = r'\/\?token=([a-zA-Z\d]+)'  # nosec
LOGIN_TOKEN_REGEXP = r'Login\s+token:\s+([a-zA-Z\d]+)'  # nosec
