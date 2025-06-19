#!/usr/bin/env bash

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js (Render needs sudo here)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Tailwind dependencies
npm install --prefix theme

# Build Tailwind CSS
python manage.py tailwind build

# Collect static files
python manage.py collectstatic --noinput
