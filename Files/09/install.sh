#!/bin/bash

# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/../.."
VENV_PATH="$PROJECT_ROOT/.venv"

# Check if virtual environment exists and works
if [ -d "$VENV_PATH" ]; then
    echo "Using existing virtual environment at $VENV_PATH"
    # Try to upgrade pip first
    "$VENV_PATH/bin/python" -m ensurepip --upgrade 2>/dev/null || true
    "$VENV_PATH/bin/python" -m pip install --upgrade pip 2>/dev/null || {
        echo "Virtual environment appears corrupted, please recreate it"
        exit 1
    }
else
    echo "No virtual environment found at $VENV_PATH"
    echo "Please create one with: python3 -m venv $VENV_PATH"
    exit 1
fi

# Install requirements
echo "Installing requirements from $SCRIPT_DIR/requirements.txt"
"$VENV_PATH/bin/pip" install -r "$SCRIPT_DIR/requirements.txt"