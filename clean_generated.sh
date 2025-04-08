#!/bin/bash

# Shell script to clean up cached generated files while running pre-commit

echo "Cleaning up generated files..."
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type d -name ".pytest_cache" -exec rm -rf {} +
find . -type d -name ".ruff_cache" -exec rm -rf {} +
find . -type d -name ".mypy_cache" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
echo "Cleanup complete."
