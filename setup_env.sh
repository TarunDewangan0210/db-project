#!/bin/bash

# Remove existing virtual environment if it exists
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Uninstall existing packages
pip uninstall -y numpy pandas psycopg2-binary pymongo python-dotenv

# Install packages with specific versions
pip install -r requirements.txt

echo "Environment setup completed. Activate the virtual environment with: source venv/bin/activate" 