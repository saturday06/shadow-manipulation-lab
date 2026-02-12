#!/bin/sh

set -eux

pid=$1
shift
start_ok_file_path=$1
shift

echo "start_ok" >"$start_ok_file_path"

for _ in $(seq 10); do
  sleep 0.2
  if ! kill -0 "$pid"; then
    break
  fi
done

exec "$@"
