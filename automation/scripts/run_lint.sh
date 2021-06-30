#!/bin/bash

while (( "$#" )); do
  case "$1" in
    -c|--lint_config)
      CONFIG=$2
      shift 2
      ;;
    -p|--path_to_package)
      PATH_TO_PACKAGE=$2
      shift 2
      ;;
    *)
      echo Unsupport argument $1
      exit 1
      ;;
  esac
done

python -m pip install pylint

python -m pip install -r ${PATH_TO_PACKAGE}/requirements-core.txt
python -m pip install -r ${PATH_TO_PACKAGE}/requirements-linux.txt

export PYTHONPATH=${PYTHONPATH}:${PATH_TO_PACKAGE}

pylint --rcfile=${CONFIG} ${PATH_TO_PACKAGE}
