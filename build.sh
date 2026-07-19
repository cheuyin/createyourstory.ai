#!/usr/bin/env bash

# Exit on error
set -o errexit

# Verify node and npm are available
node -v
npm -v

echo "Building frontend..."
npm --prefix frontend install
npm --prefix frontend run build

echo "Installing uv and backend dependencies..."
pip install uv
uv sync --project backend


