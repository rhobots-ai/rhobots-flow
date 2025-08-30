#!/bin/bash

# Rhobots Flow Setup Script
# This script helps developers customize the template for their project

set -e

echo "🚀 Rhobots Flow Setup"
echo "===================="

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "setup.py" ]; then
    echo "❌ setup.py not found. Please run this script from the project root directory."
    exit 1
fi

# Run the Python setup script
python3 setup.py

echo "✅ Setup completed!"
