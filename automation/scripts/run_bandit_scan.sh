#!/bin/bash

while (( "$#" )); do
  case "$1" in
    -o|--output_file)
      OUTPUT_FILE=$2
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

python -m pip install bandit

bandit -r ${PATH_TO_PACKAGE} -o ${OUTPUT_FILE} -f txt
