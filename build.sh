#!/usr/bin/env bash
set -euo pipefail

# Install server dependencies
pip install -r requirements.txt

# Collect static files for WhiteNoise
python manage.py collectstatic --noinput --clear

# Create media directories (after collectstatic)
mkdir -p staticfiles/media/profile_pictures

# Run database migrations
python manage.py migrate --noinput
