#!/usr/bin/env bash

set -e

BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$BRANCH" == "master" ]]; then
  VERSION=$(cat pyproject.toml | grep -Po '^\s*version\s+=\s+".+"$' | grep -Po "\d+\.\d+\.\d+(-\w+)?")
else
  VERSION=develop
fi

docker build -t topicaxis/api:${VERSION} .
