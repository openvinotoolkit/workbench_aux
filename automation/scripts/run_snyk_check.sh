#!/bin/bash

while (( "$#" )); do
  case "$1" in
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
    -no_proxy)
      NO_PROXY=$2
      shift 2
      ;;
    *)
      echo Unsupport argument $1
      exit 1
      ;;
  esac
done

OUTPUT_FILE=snyk-result.json
pushd ${PROJECT_PATH}

# Place requirements in one file
find ./ \
  -name 'requirements*.txt' \
  ! -name 'requirements_prod.txt' \
  -exec cat {} \; &> requirements_prod.txt

docker run \
  -e "http_proxy=${HTTP_PROXY}" \
  -e "https_proxy=${HTTPS_PROXY}" \
  -e "no_proxy=${NO_PROXY}" \
  -e "SNYK_TOKEN=${TOKEN}" \
  -e "SNYK_API=${SNYK_API}" \
  -v "${PROJECT_PATH}:/app" \
  --env COMMAND="pip install -r requirements_prod.txt" \
  snyk/snyk:python-3.9 \
  snyk test --json --file=requirements_prod.txt --package-manager=pip --project-name=Workbench_starter > ${OUTPUT_FILE} 2>&1
