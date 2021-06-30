#!/bin/bash

OUTPUT_FILE=snyk-result.json
PROJECT_PATH=/project

python3 -m pip install setuptools wheel

ls -la
ls -la /project

pushd ${PROJECT_PATH}

# Install project dependencies
find ./ \
  -name 'requirements*.txt' \
  -exec python3 -m pip install -r {} \;

find ./ \
  -name 'requirements*.txt' \
  -exec cat {} \; &> requirements_prod.txt

cat requirements_prod.txt

snyk test --json \
          --file=requirements_prod.txt \
          --command=python3 \
          --package-manager=pip \
          --project-name=Workbench_starter > ${OUTPUT_FILE}

cat ${OUTPUT_FILE}

exit $?
