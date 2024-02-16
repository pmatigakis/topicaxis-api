#!/usr/bin/env bash

set -e

if [ -z $1 ]; then
    echo "Declare which version part will be bumped"
    exit
fi

RELEASE_DIR=$(mktemp -d -t topicaxis-api-XXXXXXXXXX)
API_VIRTUALENV=~/.pyenv/versions/topicaxis_api_release
REPOSITORY=git@github.com:pmatigakis/topicaxis-api.git

cd $RELEASE_DIR

git clone $REPOSITORY
cd topicaxis-api
git fetch --all

git checkout master
git merge develop

pyenv virtualenv 3.10.4 topicaxis_api_release
$API_VIRTUALENV/bin/pip install poetry==1.4.2
$API_VIRTUALENV/bin/poetry config virtualenvs.create false
$API_VIRTUALENV/bin/poetry install
$API_VIRTUALENV/bin/pre-commit install
$API_VIRTUALENV/bin/pre-commit run --all-files
$API_VIRTUALENV/bin/pytest

$API_VIRTUALENV/bin/bump2version --commit --message "Released version {new_version}" --tag --tag-name "v{new_version}" $1

pyenv virtualenv-delete -f topicaxis_api_release

git push origin master --tags
git checkout develop
git merge master
git push origin develop
