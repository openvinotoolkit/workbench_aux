#!/bin/bash

while (( "$#" )); do
  case "$1" in
    -i)
      SNYK_IMAGE=$2
      shift 2
      ;;
    -p)
      PROJECT_PATH=$2
      shift 2
      ;;
    -t)
      TOKEN=$2
      shift 2
      ;;
    -a)
      SNYK_API=$2
      shift 2
      ;;
    -http_proxy)
      HTTP_PROXY=$2
      shift 2
      ;;
    -https_proxy)
      HTTPS_PROXY=$2
      shift 2
      ;;
    *)
      echo Unsupport argument $1
      exit 1
      ;;
  esac
done

set -e

docker run \
  -e "http_proxy=${HTTP_PROXY}" \
  -e "https_proxy=${HTTPS_PROXY}" \
  -e "SNYK_TOKEN=${TOKEN}" \
  -e "SNYK_API=${SNYK_API}" \
  -e "MONITOR=true" \
  -v "${PROJECT_PATH}:/project" \
  -v "/var/run/docker.sock:/var/run/docker.sock" \
  ${SNYK_IMAGE}

exit $?
