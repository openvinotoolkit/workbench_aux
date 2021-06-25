#!/bin/bash

while (( "$#" )); do
  case "$1" in
    -c|--lint_config)
      CONFIG=$2
      shift 2
      ;;
    *)
      echo Unsupport argument $1
      exit 1
      ;;
  esac
done

python -m pip install pylint

pushd /repository

export PYTHONPATH=${PYTHONPATH}:starting_package

pylint --rcfile=${CONFIG} starting_package

popd
