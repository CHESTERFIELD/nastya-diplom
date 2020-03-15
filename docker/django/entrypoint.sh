#!/bin/bash
set -e
cmd="$@"
ls

#if [ "$RUN_MIGRATE" != "" ];
#then
#    python manage.py migrate
#    python manage.py makemigrations
#    python manage.py migrate
#fi

# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate

exec $cmd
