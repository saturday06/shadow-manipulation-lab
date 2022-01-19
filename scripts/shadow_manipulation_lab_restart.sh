#!/bin/sh

set -eux

pid=$1
shift
start_ok_file_path=$1
shift

echo "start_ok" > "$start_ok_file_path"

waitpid "$pid" || true

"$@"
