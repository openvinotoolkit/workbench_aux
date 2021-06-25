#!/bin/bash

OUTPUT_FILE=snyk-result.json
MONITOR_OUTPUT_FILE=snyk-monitor-result.json
HTML_FILE=snyk_report.html
ERROR_FILE=snyk-error.log
PROJECT_FOLDER=/project

# Required by Snyk
python3 -m pip install numpy==1.16.4 cryptography==3.3.2

# Install project dependencies
python3 -m pip install -r requirements.txt

python3 -m pip install importlib

pushd ${PROJECT_FOLDER}

snyk test --json \
          --file=requirements.txt \
          --command=python3 \
          --package-manager=pip \
          --project-name=Workbench_starter > ${OUTPUT_FILE}

RC=$?

snyk monitor --json \
              --file=requirements.txt \
              --command=python3 \
              --package-manager=pip \
              --project-name=Workbench_starter > ${MONITOR_OUTPUT_FILE}


USER_ID=$(id -u)

USER_NAME=$(getent passwd "${USER_ID}" | awk -F ':' '{print $1}')

runCmdAsDockerUser() {
  su ${USER_NAME} -m -c "$1"

  return $?
}

runCmdAsDockerUser "cat ${MONITOR_OUTPUT_FILE} | jq -r 'if type==\"array\" then .[].uri? else .uri? end' | awk '{print \"<center><a target=\\\"_blank\\\" href=\\\"\" \$0 \"\\\">View On Snyk.io</a></center>\"}' > \"${HTML_FILE}\" 2>>\"${ERROR_FILE}\""

runCmdAsDockerUser "cat \"${OUTPUT_FILE}\" | \
jq 'def sortBySeverity: .vulnerabilities|= map(. + {severity_numeric: (if(.severity) == \"high\" then 1 else (if(.severity) == \"medium\" then 2 else (if(.severity) == \"low\" then 3 else 4 end) end) end)}) |.vulnerabilities |= sort_by(.severity_numeric) | del(.vulnerabilities[].severity_numeric); if (. | type) == \"array\" then map(sortBySeverity) else sortBySeverity end'| \
snyk-to-html | \
sed 's/<\/head>/  <link rel=\"stylesheet\" href=\"snyk_report.css\"><\/head>/' \
>> \"${HTML_FILE}\""

exit "$RC"
