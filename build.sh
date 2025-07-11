#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # Exit on error

# Set environment variables for Render
export FLASK_ENV=render
export FLASK_APP=run.py

# Install Python dependencies
pip install -r requirements-render.txt

# Run database migrations
flask db upgrade

# Create initial data (if needed)
if [ "$FLASK_ENV" = "render" ]; then
    echo "Loading seed data for Render production"
    python scripts/seed_data.py
else
    python scripts/seed_data.py
fi

echo "Build completed successfully!"