#!/usr/bin/bash

# Requires pyinstaller, python3, and bash.

rm -rf build/ >> /dev/null 2>&1
rm -rf dist/ >> /dev/null 2>&1

pyinstaller --onefile main.py

