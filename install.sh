#!/bin/bash

echo "Installing reza-fastmcp server dependencies..."

# Check if we're in a virtual environment
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installation complete!"
echo "To run the server:"
echo "  source venv/bin/activate  # if not already activated"
echo "  python server.py"