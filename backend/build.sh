#!/usr/bin/env bash
# build.sh

set -o errexit  # exit on error

# Upgrade pip and install build tools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install -r requirements.txt