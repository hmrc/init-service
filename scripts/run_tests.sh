#!/bin/bash

py.test -v --junitxml results.xml test/tests.py
test/integration-tests.py
