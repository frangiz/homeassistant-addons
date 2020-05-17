#!/usr/bin/env bash

set -e

cd "$(readlink -f "$(dirname "$0")")" || exit 9

if [[ "$1" == build ]]
then
  build_cmd="docker build . \
    --build-arg BUILD_FROM=homeassistant/amd64-base-debian:buster \
    -t frangiz/homeassistant-walter-amd64:latest"
  eval "$build_cmd"
elif [[ "$1" == start ]]
then
  start_cmd="docker run --rm --name walter frangiz/homeassistant-walter-amd64:latest"
  eval "$start_cmd"
elif [[ "$1" == stop ]]
then
  stop_cmd="docker stop walter"
  eval "$stop_cmd"
else
  echo "Usage: $(basename "$0") [build,start,stop]"
  exit 2
fi