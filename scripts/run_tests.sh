#!/bin/bash

python -m pytest -v --junitxml results.xml test/tests.py
test/integration-tests.py
