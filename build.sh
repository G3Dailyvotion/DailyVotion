#!/usr/bin/env bash
set -euo pipefail

# Install server dependencies
pip install -r requirements.txt

# Create media directories (will be filled by collectstatic in buildCommand)
mkdir -p staticfiles/media/profile_pictures

# Run database migrations
python manage.py migrate --noinput
