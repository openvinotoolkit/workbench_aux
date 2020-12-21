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

_print_is_enabled() {
    ENABLED=$([[ -n "$2" ]] && echo "True" || echo "False")
    echo "$1: ${ENABLED}"
}

HTTP_PROXY=${http_proxy}
HTTPS_PROXY=${https_proxy}
NO_PROXY=${no_proxy}

help_message="Usage: start_workbench.sh -IMAGE_NAME \${image_name}
                                       [-HTTP_PROXY \${http_proxy}]
                                       [-HTTPS_PROXY \${https_proxy}]
                                       [-NO_PROXY \${no_proxy}]
                                       [-OTHER_ARGUMENTS]

\e[1mOptional parameters:\e[0m

    -IMAGE_NAME - Specifies the name of the image to build the Docker container upon. Default value: 'workbench'.
    -ASSETS_DIR - Mounts a provided local folder to the '/home/workbench/.workbench' directory in the Docker container. The folder is not mounted by default. Format: /path/to/dir
    -DETACHED - Runs DL Workbench in detached mode. Default value: 'false'.
    -RESTART - Restarts a previously stopped DL Workbench container. Example: '-RESTART <container-name>'.
    -STOP - Stops a DL Workbench container. Example: '-STOP <container-name>'.
    -IP - Specifies the IP to bind. Default value: '0.0.0.0'.
    -PORT - Maps the Docker container port '5665' to the provided host port to get access to the DL Workbench from a web browser. Default value: '5665'.
    -TAG - Specifies the tag to use. Default is '2021.2'.
    -CONTAINER_NAME - Specifies the name of a container. Default value: 'workbench'.
    -HTTP_PROXY - Specifies the HTTP proxy. Format:  'http://<user>:<password>@<proxy-host>:<proxy-port>'.
    -HTTPS_PROXY - Specifies the HTTPS proxy. Format:  'https://<user>:<password>@<proxy-host>:<proxy-port>'.
    -NO_PROXY - Specifies URLs to be excluded from proxying. Format: 'url1,url2,url31'.
    -SSL_CERT - Specifies the path to the DL Workbench web app TLS certificate in the DL Workbench assets directory. Example: /'ASSETS_DIR'/certificate.pem
    -SSL_KEY - Specifies the path to the 'SSL_CERT' certificate private key in the DL Workbench assets directory. Example: /'ASSETS_DIR'/key.pem
    -SSL_VERIFY - Sets the 'SSL_CERT' TLS certificate as trusted ('true'), self-signed ('false'), or untrusted ('false'). Default: 'true'.
    -CLOUD_SERVICE_URL - Specifies the URL to a standalone cloud service that provides Intel(R) hardware capabilities for experiments.
    -CLOUD_SERVICE_SESSION_TTL_MINUTES - Specifies the cloud service session time to live minutes.
    -NETWORK_NAME - Specifies the name of a Docker network to run the Docker container in. Default name: 'workbench_network'.
    -NETWORK_ALIAS - Specifies the alias of the DL Workbench container in the network. Default alias: 'workbench'.

\e[1mArguments that enable devices (by default, only CPU is enabled):\e[0m

    -ENABLE_GPU - Specifies whether to enable GPU. Default value: 'false'.
    -ENABLE_MYRIAD - Specifies whether to enable MYRIAD. Default value: 'false'.
    -ENABLE_HDDL - Specifies whether to enable HDDL. Default value: 'false'.

\e[1mRestart previously stopped DL Workbench container:\e[0m

./start_workbench.sh -RESTART <container-name>

\e[31mOther arguments (except -DETACHED) are not supported. DL Workbench will have the capabilities that were enabled on the first run.\e[0m

\e[1mNotes:\e[0m

1. '-ENABLE_MYRIAD' and '-ENABLE_HDDL' arguments cannot be set simultaneously.

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl

2. If you want to save login token to a local file, provide 'ASSETS_DIR' argument.
"

hddl_myriad_help_message="
'-ENABLE_MYRIAD' and '-ENABLE_HDDL' arguments cannot be set simultaneously.

\e[1mAborting.\e[0m

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl
"

hddl_help_message="
hddldaemon is not running in the background.

\e[1mAborting.\e[0m

See documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Install_from_Docker_Hub.html#cpu-hddl
"

permissions_help_message="
Provided assets directory does not have required permissions. Read, write, and execute permissions are required for 'others' group (at least **7 mode).

Create the required configuration directory with the following command:

mkdir -p -m 777 /path/to/dir

Then copy the required assets into it and and mount the directory by assigning it to the '-ASSETS_DIR' argument.

\e[31mNOTE: Execution of the above command creates a directory accessible to ALL users for reading, writing, and executing.

\e[0mSee documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Troubleshooting.html#container
"

no_directory_help_message="
Provided assets directory does not exist.

Create the required configuration directory with the following command:

mkdir -p -m 777 /path/to/dir

Then copy the required assets into it and use the directory as '-ASSETS_DIR' argument.

\e[31mNOTE: Execution of the above command creates a directory accessible to ALL users for reading, writing, and executing.

\e[0mSee documentation for additional info:
https://docs.openvinotoolkit.org/latest/_docs_Workbench_DG_Troubleshooting.html#container
"

restarting_container_help_message="
Could not recognize the arguments provided to restart the DL Workbench container. To restart the container, provide only the container name.

./start_workbench.sh -RESTART <container-name>

\e[31mOther arguments (except -DETACHED) are not supported. DL Workbench will have the capabilities that were enabled on the first run.\e[0m
"

stopping_container_help_message="
Could not recognize the arguments provided to stop the DL Workbench container. To stop the container, provide only the container name.

./start_workbench.sh -STOP <container-name>

\e[31mOther arguments are not supported. The DL Workbench will be stopped.\e[0m
"

# Verify args if restart is needed
if [[ "$@" == *'-RESTART'* ]]; then
    if [[ "$@" == *'-DETACHED'* ]] && [[ $# -ne 3 ]]; then # Maximum 3 args
        echo -e "$restarting_container_help_message"
        exit 1
    elif [[ ! "$@" == *'-DETACHED'* ]] && [[ $# -ne 2 ]]; then # Maximum 2 args
        echo -e "$restarting_container_help_message"
        exit 1
    fi
fi

# Verify args if stop is needed
if [[ "$@" == *'-STOP'* ]] && [[ ! $# -eq 2 ]]; then # Maximum 2 args
    echo -e "$stopping_container_help_message"
    exit 1
fi

export SSL_VERIFY=on

while test $# -gt 0; do
    case "$1" in
        -HELP|--help|-help)
            echo -e "$help_message"
            exit 1
            ;;
        -HTTP_PROXY)
            HTTP_PROXY=$2
            shift 2
            ;;
        -HTTPS_PROXY)
            HTTPS_PROXY=$2
            shift 2
            ;;
        -NO_PROXY)
            NO_PROXY=$2
            shift 2
            ;;
        -ASSETS_DIR)
            ASSETS_DIR=$2
            SAVE_TOKEN=1
            shift 2
            ;;
        -SSL_CERT)
            SSL_CERT=$2
            shift 2
            ;;
        -SSL_KEY)
            SSL_KEY=$2
            shift 2
            ;;
        -SSL_VERIFY)
            export SSL_VERIFY=$2
            shift 2
            ;;
        -IMAGE_NAME)
            IMAGE_NAME=$2
            shift 2
            ;;
        -TAG)
            TAG=$2
            shift 2
            ;;
        -IP)
            IP=$2
            shift 2
            ;;
        -PORT)
            PORT=$2
            shift 2
            ;;
        -DETACHED)
            DETACHED="-d"
            shift
            ;;
        -RESTART)
            CONTAINER_TO_RESTART=$2
            shift 2
            ;;
        -STOP)
            CONTAINER_TO_STOP=$2
            shift 2
            ;;
        -CONTAINER_NAME)
            CONTAINER_NAME=$2
            shift 2
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
        -NETWORK_NAME)
            NETWORK_NAME=$2
            shift 2
            ;;
        -NETWORK_ALIAS)
            NETWORK_ALIAS=$2
            shift 2
            ;;
        -DISABLE_ANALYTICS)
            DISABLE_ANALYTICS=1
            shift
            ;;
        -CLOUD_SERVICE_URL)
            CLOUD_SERVICE_URL=$2
            shift 2
            ;;
        -CLOUD_SERVICE_SESSION_TTL_MINUTES)
            CLOUD_SERVICE_SESSION_TTL_MINUTES=$2
            shift 2
            ;;
        *)
            echo -e "$help_message"
            exit 1
            ;;
    esac
done

# Stop container
if [[ -n ${CONTAINER_TO_STOP} ]]; then
    if [[ -n "$(docker ps | grep ${CONTAINER_TO_STOP})" ]]; then # Check if container is running
        echo "A container with the name '${CONTAINER_TO_STOP}' is running."
        echo "Stopping the container..."
        docker stop ${CONTAINER_TO_STOP}
        echo "The container was stopped."
        exit 0
    else
        echo "A container with the name '${CONTAINER_TO_STOP}' does not exist or is not running."
        echo "Use ./start_workbench.sh --help for available arguments."
        echo -e "\e[1mAborting.\e[0m"
        exit 1
    fi
fi

# Restart previously stopped container
if [[ -n ${CONTAINER_TO_RESTART} ]]; then
    echo "Restarting a previously stopped container..."

    # Check for container presence
    if [[ -n "$(docker ps | grep ${CONTAINER_TO_RESTART})" ]]; then # Check if container is running
        echo "A container with the name '${CONTAINER_TO_RESTART}' is running."
        echo "Stop it and try again."
        echo -e "\e[1mAborting.\e[0m"
        exit 1
    elif [[ -z "$(docker ps -a | grep ${CONTAINER_TO_RESTART})" ]]; then # Check if container does not exist
        echo "A container with the name '${CONTAINER_TO_RESTART}' does not exist."
        echo "Use ./start_workbench.sh --help for details."
        echo -e "\e[1mAborting.\e[0m"
        exit 1
    fi

    # Restart
    if [[ -n ${DETACHED} ]]; then # Restarting in detached mode
        docker start ${CONTAINER_TO_RESTART}
        echo "A container was restarted in detached mode."
        exit 0
    else # Restarting in interactive mode
        docker start -ai ${CONTAINER_TO_RESTART}
        exit 0
    fi
fi

# Specify image name
IMAGE_NAME=${IMAGE_NAME:-"openvino/workbench"}

# Specify tag, current release
TAG=${TAG:-"2021.2"}

# Verify that image exists
docker inspect --type=image ${IMAGE_NAME}:${TAG} > /dev/null 2>&1
if [[ $? -ne 0 ]]; then
    echo "An image with the specified name '${IMAGE_NAME}' and tag '${TAG}' was not found locally. Trying to pull it from Docker Hub..."

    docker pull ${IMAGE_NAME}:${TAG}

    if [[ $? -ne 0 ]]; then
        echo ""
        echo "Could not pull the image from Docker Hub."
        echo "Pull and start the highest available version of the DL Workbench with 'openvino/workbench' as IMAGE_NAME and 'latest' as TAG."
        echo "./start_workbench.sh -IMAGE_NAME openvino/workbench -TAG latest"
        echo -e "\e[31mNOTE: All your current DL Workbench projects will be lost if you run the new version.\e[0m"
        exit 1
    fi
fi

# Specify IP
IP=${IP:-"0.0.0.0"}

# Specify port
PORT=${PORT:-5665}
WORKBENCH_INSIDE_PORT=5665

# Specify container name
CONTAINER_NAME=${CONTAINER_NAME:-"workbench"}

# Check if HDDL & MYRIAD are set simultaneously
if [[ ${ENABLE_MYRIAD} -gt 0 ]] && [[ -n "${ENABLE_HDDL}" ]]; then
    echo -e "${hddl_myriad_help_message}"
    exit 1
fi

# Check if hddldaemon is running in the background
hddl_processes=$(ps -ef | grep -v grep | grep -c hddl)

if [[ -n "${ENABLE_HDDL}" ]] && [[ ${hddl_processes} -eq 0 ]]; then
    echo -e "${hddl_help_message}"
    exit 1
fi

# Verify assets directory
if [[ -n ${ASSETS_DIR} ]] && [[ "$OSTYPE" != "darwin"* ]]; then
    if [[ -d ${ASSETS_DIR} ]]; then
        PERMISSIONS=$(stat -c "%a" ${ASSETS_DIR})
        OTHER_PERMISSIONS="${PERMISSIONS:2:1}" # Taking the third number, which is permissions for 'others'

        if [[ ${OTHER_PERMISSIONS} -ne 7 ]] && [[ ${OTHER_PERMISSIONS} -ne 6 ]]; then
            echo "Assets directory: ${ASSETS_DIR}"
            echo "Permissions: ${PERMISSIONS}"
            echo -e "${permissions_help_message}"
            exit 1
        fi
    else
        echo -e "${no_directory_help_message}"
        exit 1
    fi
fi

# Convert paths to Docker directory layout
DOCKER_CONFIG_DIR=/home/workbench/.workbench
if [ ! -z ${SSL_KEY} ] && [[ ! -f ${SSL_KEY} ]]; then
    echo "${SSL_KEY} is not found in ${ASSETS_DIR}."
    echo -e "\e[1mAborting.\e[0m"
    exit 1
elif [[ -f ${SSL_KEY} ]]; then
    SSL_KEY="${DOCKER_CONFIG_DIR}/$(realpath --relative-to "${ASSETS_DIR}" "$SSL_KEY")"
fi

if [ ! -z ${SSL_CERT} ] && [[ ! -f ${SSL_CERT} ]]; then
    echo "${SSL_CERT} is not found in ${ASSETS_DIR}."
    echo -e "\e[1mAborting.\e[0m"
    exit 1
elif [[ -f ${SSL_CERT} ]]; then
    SSL_CERT="${DOCKER_CONFIG_DIR}/$(realpath --relative-to "${ASSETS_DIR}" "$SSL_CERT")"
fi

# Check that there are no containers with the same name
if [ "$(docker ps -a | grep ${CONTAINER_NAME})" ]; then
    echo "Stopping the old DL Workbench Docker container."
    docker stop ${CONTAINER_NAME}
    echo "Removing the old DL Workbench Docker container."
    docker rm ${CONTAINER_NAME}
fi

# Check that there is a Docker network with the name $NETWORK_NAME
NETWORK_NAME=${NETWORK_NAME:-"workbench_network"}
NETWORK_ALIAS=${NETWORK_ALIAS:-"workbench"}
if [ ! "$(docker network ls --filter name=${NETWORK_NAME} --format \"{{.Name}}\")" ]; then
    docker network create -d bridge ${NETWORK_NAME}
fi

set -e

# Transform each Boolean argument if it was not set
DETACHED=${DETACHED:-" "}
ENABLE_GPU=${ENABLE_GPU:-" "}
ENABLE_HDDL=${ENABLE_HDDL:-" "}
DISABLE_ANALYTICS=${DISABLE_ANALYTICS:-"0"}

# Display set arguments
echo ""
echo -e "\e[1mStarting the DL Workbench with the following arguments:\e[0m"
echo "Image Name: ${IMAGE_NAME}"
echo "Tag: ${TAG}"
echo "Container Name: ${CONTAINER_NAME}"
echo "IP: ${IP}"
echo "Port: ${PORT}"
if [[ -n ${ASSETS_DIR} ]]; then
    ASSETS_DIR=${ASSETS_DIR%/}
    echo "Assets Directory: ${ASSETS_DIR}"
    echo "Token File: ${ASSETS_DIR}/token.txt"
fi
_print_is_enabled "Detached" ${DETACHED}
_print_is_enabled "GPU Enabled" ${ENABLE_GPU}
_print_is_enabled "MYRIAD Enabled" ${ENABLE_MYRIAD}
_print_is_enabled "HDDL Enabled" ${ENABLE_HDDL}
echo ""


if [[ ${ENABLE_MYRIAD} -gt 0 ]]; then
    docker run -p ${IP}:${PORT}:${WORKBENCH_INSIDE_PORT} \
            --name ${CONTAINER_NAME} \
            ${DETACHED} \
            ${ENABLE_GPU} \
            --device-cgroup-rule='c 189:* rmw' \
            -v /dev/bus/usb:/dev/bus/usb \
            $([ -z ${ASSETS_DIR+x} ] || printf -- '-v %s\n' ${ASSETS_DIR}:${DOCKER_CONFIG_DIR} ) \
            -e http_proxy="${HTTP_PROXY}" \
            -e https_proxy="${HTTPS_PROXY}" \
            -e no_proxy="${NO_PROXY}" \
            -e DISABLE_ANALYTICS=${DISABLE_ANALYTICS} \
            -e PUBLIC_PORT=${PORT} \
            $([ -z ${SAVE_TOKEN+x} ] || printf -- '-e %s\n' SAVE_TOKEN_TO_FILE=1 ) \
            $([ -z ${SSL_KEY+x} ] || printf -- '-e %s\n' SSL_KEY=$SSL_KEY ) \
            $([ -z ${SSL_CERT+x} ] || printf -- '-e %s\n' SSL_CERT=$SSL_CERT ) \
            $([ -z ${SSL_VERIFY+x} ] || printf -- '-e %s\n' SSL_VERIFY=$SSL_VERIFY ) \
            $([ -z ${CLOUD_SERVICE_URL+x} ] || printf -- '-e %s\n' CLOUD_SERVICE_URL=${CLOUD_SERVICE_URL} ) \
            $([ -z ${CLOUD_SERVICE_SESSION_TTL_MINUTES+x} ] || printf -- '-e %s\n' CLOUD_SERVICE_SESSION_TTL_MINUTES=${CLOUD_SERVICE_SESSION_TTL_MINUTES} ) \
            -e NETWORK_ALIAS=${NETWORK_ALIAS} \
            --network=${NETWORK_NAME} \
            --network-alias=${NETWORK_ALIAS} \
            -it ${IMAGE_NAME}:${TAG}
else
    docker run -p ${IP}:${PORT}:${WORKBENCH_INSIDE_PORT} \
            --name ${CONTAINER_NAME} \
            ${DETACHED} \
            ${ENABLE_GPU} \
            ${ENABLE_HDDL} \
            $([ -z ${ASSETS_DIR+x} ] || printf -- '-v %s\n' ${ASSETS_DIR}:${DOCKER_CONFIG_DIR} ) \
            -e http_proxy="${HTTP_PROXY}" \
            -e https_proxy="${HTTPS_PROXY}" \
            -e no_proxy="${NO_PROXY}" \
            -e DISABLE_ANALYTICS=${DISABLE_ANALYTICS} \
            -e PUBLIC_PORT=${PORT} \
            $([ -z ${SAVE_TOKEN+x} ] || printf -- '-e %s\n' SAVE_TOKEN_TO_FILE=1 ) \
            $([ -z ${SSL_KEY+x} ] || printf -- '-e %s\n' SSL_KEY=$SSL_KEY ) \
            $([ -z ${SSL_CERT+x} ] || printf -- '-e %s\n' SSL_CERT=$SSL_CERT ) \
            $([ -z ${SSL_VERIFY+x} ] || printf -- '-e %s\n' SSL_VERIFY=$SSL_VERIFY ) \
            $([ -z ${CLOUD_SERVICE_URL+x} ] || printf -- '-e %s\n' CLOUD_SERVICE_URL=${CLOUD_SERVICE_URL} ) \
            $([ -z ${CLOUD_SERVICE_SESSION_TTL_MINUTES+x} ] || printf -- '-e %s\n' CLOUD_SERVICE_SESSION_TTL_MINUTES=${CLOUD_SERVICE_SESSION_TTL_MINUTES} ) \
            -e NETWORK_ALIAS=${NETWORK_ALIAS} \
            --network=${NETWORK_NAME} \
            --network-alias=${NETWORK_ALIAS} \
            -it ${IMAGE_NAME}:${TAG}
fi

# Show url and token if container is in detached mode
if [[ ! $DETACHED =~ ^\ +$ ]]; then
    PREFIX=http
    if [[ -f ${SSL_CERT} ]] && [[ -f ${SSL_KEY} ]]; then
        PREFIX=https
    fi

    echo ""
    echo "DL Workbench is available at: ${PREFIX}://127.0.0.1:${PORT}"

    if [[ -f "${ASSETS_DIR}/token.txt" ]]; then
        echo "Login token: $(cat "${ASSETS_DIR}/token.txt")"
    fi
fi
