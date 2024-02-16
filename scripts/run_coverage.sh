#!/usr/bin/env bash

coverage run -m pytest
coverage html -d cover
