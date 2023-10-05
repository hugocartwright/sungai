#!/bin/bash
pip install -r requirements-dev.txt --no-cache-dir
pip install sungai -e .
pre-commit install
