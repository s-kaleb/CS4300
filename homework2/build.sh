#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python movie_theater_booking/manage.py collectstatic --no-input

python movie_theater_booking/manage.py migrate

python movie_theater_booking/manage.py createsuperuser --noinput || true