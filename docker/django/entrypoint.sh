#!/bin/bash
set -e
cmd="$@"
ls

if [ "$RUN_MIGRATE" != "" ];
then
    python manage.py migrate --noinput
fi

# if [ "$RUN_MIGRATE" != "" ];
# then
#     python manage.py runserver 8000
# fi

exec $cmd
