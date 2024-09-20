#!/bin/bash
#******************************************************************************
# Copyright (c) 2024, Custom Discoveries Inc.
# All rights reserved.
#installPythonEnvironment.sh: Bash shell seteup python3 Virtual Environment
#******************************************************************************
version=3.10
echo "***************************************"
echo "Installing Python Environment $version (.venv)"
echo "***************************************"

echo `python$version -V`

if [ -d `pwd`/.venv ]; then
  #echo "run at command prompt: source \`pwd\`/.venv/bin/activate"
  source `pwd`/.venv/bin/activate
else
  echo "***************************************"
  echo "Creating .venv Environment...for Python Verson: $version"
  echo "Installing requirements.txt"
  echo "***************************************"
  python$version -m venv `pwd`/.venv
  source `pwd`/.venv/bin/activate
  pip install --upgrade pip
  pip install -U -r requirements.txt
fi
