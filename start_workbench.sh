#!/bin/bash
# Copyright (c) 2018-2019 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

HTTP_PROXY=${http_proxy}
HTTPS_PROXY=${https_proxy}
NO_PROXY=${no_proxy}

help_message="Usage -IMAGE_NAME \${image_name}
                    [-HTTP_PROXY \${http_proxy}]
                    [-HTTPS_PROXY \${https_proxy}]
                    [-NO_PROXY \${no_proxy}]
                    [-OTHER_ARGUMENTS]

Optional parameters:

    -IMAGE_NAME - Specifies the name of the image to build the Docker container upon. Default value: 'openvino/workbench'.
    -ASSETS_DIR - Mounts a provided local folder to the '/home/openvino/.workbench' directory in the Docker container. The folder is not mounted by default.
    -DETACHED - Runs DL Workbench in detached mode. Default value: 'false'.
    -IP - Specifies the IP to bind. Default value: '0.0.0.0'.
    -PORT - Maps the Docker container port '5665' to the provided host port to get access to the DL Workbench from a web browser. Default value: '5665'.
    -TAG - Specifies the tag to use. Default value: 'latest'.
    -CONTAINER_NAME - Specifies the name of container. Default value: 'workbench'.
    -SAVE_TOKEN - Enables saving of login token to a file. Default value: 'false'.
    -HTTP_PROXY - Specifies HTTP proxy in format:  'http://<user>:<password>@<proxy-host>:<proxy-port>'.
    -HTTPS_PROXY - Specifies HTTPS proxy in format:  'https://<user>:<password>@<proxy-host>:<proxy-port>'.
    -NO_PROXY - Specifies URLs to be excluded from proxying in format: 'url1,url2,url31'.
    -SSL_CERT - Specifies path to DL Workbench web app TLS certificate in DL Workbench assets directory. Example: /'ASSETS_DIR'/certificate.pem
    -SSL_KEY - Specifies path to 'SSL_CERT' certificate private key in DL Workbench assets directory. Example: /'ASSETS_DIR'/key.pem
    -SSL_VERIFY - Sets 'SSL_CERT' TLS certificate as trusted ('on', default), or either self-signed or untrusted ('off').

Arguments that enable devices (by default, only CPU is enabled):

    -ENABLE_GPU - Specifies whether to enable GPU. Default value: 'false'.
    -ENABLE_MYRIAD - Specifies whether to enable MYRIAD. Default value: 'false'.
    -ENABLE_HDDL - Specifies whether to enable HDDL. Default value: 'false'.

Notes:

1. '-ENABLE_MYRIAD' and '-ENABLE_HDDL' arguments cannot be set simultaneously. See documentation for additional info.

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl

2. If you want to save login token, provide 'ASSETS_DIR' argument as well.
"

hddl_myriad_help_message="
'-ENABLE_MYRIAD' and '-ENABLE_HDDL' arguments cannot be set simultaneously.

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl
"

hddl_help_message="
hddldaemon is not running in the background.

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl
"

permissions_help_message="
Provided assets directory does not have required permissions. Read, write, and execute permissions are required for 'others' group (at least **7 mode).

Please create the required configuration directory with the following command:

mkdir -p -m 777 /path/to/dir

Then copy the required assets into it and and mount the directory by assigning it to the '-ASSETS_DIR' argument.

\e[31mNOTE: Execution of the above command creates a directory accessible to ALL users for reading, writing, and executing.

\e[0mSee documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Troubleshooting.html#container
"

no_directory_help_message="
Provided assets directory does not exist.

Please create the required configuration directory with the following command:

mkdir -p -m 777 /path/to/dir

Then copy the required assets into it and use the directory as '-ASSETS_DIR' argument.

\e[31mNOTE: Execution of the above command creates a directory accessible to ALL users for reading, writing, and executing.

\e[0mSee documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Troubleshooting.html#container
"


export SSL_VERIFY=on

while test $# -gt 0; do
    case "$1" in
        -HELP|--help|-help)
            echo "$help_message"
            exit -1
            ;;
        -HTTP_PROXY)
            shift
            HTTP_PROXY=$1
            shift
            ;;
        -HTTPS_PROXY)
            shift
            HTTPS_PROXY=$1
            shift
            ;;
        -NO_PROXY)
            shift
            NO_PROXY=$1
            shift
            ;;
        -ASSETS_DIR)
            shift
            ASSETS_DIR=$1
            shift
            ;;
        -SSL_CERT)
            shift
            SSL_CERT=$1
            shift
            ;;
        -SSL_KEY)
            shift
            SSL_KEY=$1
            shift
            ;;
        -SSL_VERIFY)
            shift
            export SSL_VERIFY=$1
            shift
            ;;
        -IMAGE_NAME)
            shift
            IMAGE_NAME=$1
            shift
            ;;
        -TAG)
            shift
            TAG=$1
            shift
            ;;
        -IP)
            shift
            IP=$1
            shift
            ;;
        -PORT)
            shift
            PORT=$1
            shift
            ;;
        -SAVE_TOKEN)
            SAVE_TOKEN=1
            shift
            ;;
        -DETACHED)
            DETACHED="-d"
            shift
            ;;
        -CONTAINER_NAME)
            shift
            CONTAINER_NAME=$1
            shift
            ;;
        -ENABLE_GPU)
            ENABLE_GPU="--device /dev/dri"
            shift
            ;;
        -ENABLE_MYRIAD)
            ENABLE_MYRIAD=1
            shift
            ;;
        -ENABLE_HDDL)
            ENABLE_HDDL="--device=/dev/ion:/dev/ion -v /var/tmp:/var/tmp"
            shift
            ;;
        *)
            echo "$help_message"
            exit -1
            ;;
    esac
done

# Specify image name
IMAGE_NAME=${IMAGE_NAME:-"openvino/workbench"}

# Specify IP
IP=${IP:-"0.0.0.0"}

# Specify port
PORT=${PORT:-5665}

# Specify container name
CONTAINER_NAME=${CONTAINER_NAME:-workbench}

# Specify tag
TAG=${TAG:-latest}

# Check if HDDL & MYRIAD are set simultaneously
if [[ ${ENABLE_MYRIAD} -gt 0 ]] && [[ -n "${ENABLE_HDDL}" ]]; then
    echo "${hddl_myriad_help_message}"
    exit 1
fi

# Check if hddldaemon is running in the background
hddl_processes=$(ps -ef | grep -v grep | grep -c hddl)

if [[ -n "${ENABLE_HDDL}" ]] && [[ ${hddl_processes} -eq 0 ]]; then
    echo "${hddl_help_message}"
    exit 1
fi

# Verify assets directory
if [[ -n ${ASSETS_DIR} ]]; then

    if [[ -d ${ASSETS_DIR} ]]; then
        PERMISSIONS=$(stat -c "%a" ${ASSETS_DIR})
        OTHERS_PERMISSIONS="${PERMISSIONS:2:1}" # Taking the third number, which is permissions for 'others'

        if [[ ${OTHERS_PERMISSIONS} -ne 7 ]] && [[ ${OTHERS_PERMISSIONS} -ne 6 ]]; then
            echo "Assets directory: ${ASSETS_DIR}"
            echo "Permissions: ${PERMISSIONS}"
            echo -e "${permissions_help_message}"
            echo "Aborting."
            exit 1
        fi
    else
        echo -e "${no_directory_help_message}"
        echo "Aborting."
        exit 1
    fi
fi

# Check if token saving is enabled and ASSETS_DIR is provided
if [[ ${SAVE_TOKEN} -eq 1 ]] && [[ -z ${ASSETS_DIR} ]]; then
    echo "To save login token, provide the save directory as the 'ASSETS_DIR' argument."
    echo "Aborting."
    exit 1
fi

# Convert paths to Docker directory layout
DOCKER_CONFIG_DIR=/home/openvino/.workbench
if [ ! -z ${SSL_KEY} ] && [[ ! -f ${SSL_KEY} ]]; then
    echo "${SSL_KEY} is not found in ${ASSETS_DIR}."
    exit 1
elif [[ -f ${SSL_KEY} ]]; then
    SSL_KEY="${DOCKER_CONFIG_DIR}/$(realpath --relative-to "${ASSETS_DIR}" "$SSL_KEY")"
fi

if [ ! -z ${SSL_CERT} ] && [[ ! -f ${SSL_CERT} ]]; then
    echo "${SSL_CERT} is not found in ${ASSETS_DIR}."
    exit 1
elif [[ -f ${SSL_CERT} ]]; then
    SSL_CERT="${DOCKER_CONFIG_DIR}/$(realpath --relative-to "${ASSETS_DIR}" "$SSL_CERT")"
fi

# Check that there are no containers with the same name
if [ "$(docker ps -a | grep ${CONTAINER_NAME})" ]; then
    echo "Stop old DL Workbench Docker container."
    docker stop ${CONTAINER_NAME}
    echo "Remove old DL Workbench Docker container."
    docker rm ${CONTAINER_NAME}
fi

set -e

# Transform each Boolean argument if it was not set
DETACHED=${DETACHED:-" "}
ENABLE_GPU=${ENABLE_GPU:-" "}
ENABLE_HDDL=${ENABLE_HDDL:-" "}

if [[ ${ENABLE_MYRIAD} -gt 0 ]]; then
    docker run -p ${IP}:${PORT}:5665 \
            --name ${CONTAINER_NAME} \
            ${DETACHED} \
            ${ENABLE_GPU} \
            --device-cgroup-rule='c 189:* rmw' \
            -v /dev/bus/usb:/dev/bus/usb \
            $([ -z ${ASSETS_DIR+x} ] || printf -- '-v %s\n' ${ASSETS_DIR}:${DOCKER_CONFIG_DIR} ) \
            -e http_proxy="${HTTP_PROXY}" \
            -e https_proxy="${HTTPS_PROXY}" \
            -e no_proxy="${NO_PROXY}" \
            $([ -z ${SAVE_TOKEN+x} ] || printf -- '-e %s\n' SAVE_TOKEN_TO_FILE=1 ) \
            $([ -z ${SSL_KEY+x} ] || printf -- '-e %s\n' SSL_KEY=$SSL_KEY ) \
            $([ -z ${SSL_CERT+x} ] || printf -- '-e %s\n' SSL_CERT=$SSL_CERT ) \
            $([ -z ${SSL_VERIFY+x} ] || printf -- '-e %s\n' SSL_VERIFY=$SSL_VERIFY ) \
            -it ${IMAGE_NAME}:${TAG}
else
    docker run -p ${IP}:${PORT}:5665 \
            --name ${CONTAINER_NAME} \
            ${DETACHED} \
            ${ENABLE_GPU} \
            ${ENABLE_HDDL} \
            $([ -z ${ASSETS_DIR+x} ] || printf -- '-v %s\n' ${ASSETS_DIR}:${DOCKER_CONFIG_DIR} ) \
            -e http_proxy="${HTTP_PROXY}" \
            -e https_proxy="${HTTPS_PROXY}" \
            -e no_proxy="${NO_PROXY}" \
            $([ -z ${SAVE_TOKEN+x} ] || printf -- '-e %s\n' SAVE_TOKEN_TO_FILE=1 ) \
            $([ -z ${SSL_KEY+x} ] || printf -- '-e %s\n' SSL_KEY=$SSL_KEY ) \
            $([ -z ${SSL_CERT+x} ] || printf -- '-e %s\n' SSL_CERT=$SSL_CERT ) \
            $([ -z ${SSL_VERIFY+x} ] || printf -- '-e %s\n' SSL_VERIFY=$SSL_VERIFY ) \
            -it ${IMAGE_NAME}:${TAG}
fi
