#!/usr/bin/env bash

# Get the full path of the current script
full_path=$(realpath $0)

# Get the directory path of the current script
dir_path=$(dirname $full_path)

# Construct the path to the Python script
python_script_path="$dir_path/src/__main__.py"

# Execute the Python script
python3 $python_script_path $@
