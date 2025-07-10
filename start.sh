#!/usr/bin/env bash
# Start script for Render deployment

set -o errexit  # Exit on error

# Start the Flask application with Gunicorn
gunicorn --bind 0.0.0.0:$PORT --workers 4 --timeout 120 run:app