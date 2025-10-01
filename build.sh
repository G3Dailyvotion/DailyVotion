#!/usr/bin/env bash
set -euo pipefail

# Install server dependencies
pip install -r requirements.txt

# Create media directories
mkdir -p staticfiles/media/profile_pictures

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate --noinput
