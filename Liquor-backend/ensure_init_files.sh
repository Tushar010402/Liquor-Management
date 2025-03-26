#!/bin/bash

# Create __init__.py files in all directories to make them proper Python packages
find src -type d -exec touch {}/__init__.py \; 2>/dev/null || true

# Set permissions
chmod -R 755 src

echo "Created __init__.py files in all directories" 