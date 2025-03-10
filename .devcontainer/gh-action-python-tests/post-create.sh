#!/bin/sh

pip install -r tests/requirements.txt

playwright install-deps

playwright install
