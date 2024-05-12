#!/bin/bash

get_abs_dir="$(dirname "$(readlink -f "$0")")"
abs_app_dir="$get_abs_dir/app"

export PYTHONPATH="$abs_app_dir:$PYTHONPATH"

pytest "$@"