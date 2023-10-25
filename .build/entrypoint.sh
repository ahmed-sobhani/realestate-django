#!/bin/sh

set -e

wait_for() {
    /wait-for.sh ${DB_HOST}:${DB_PORT}
}


if [ "$1" == "rest" ]
then
    wait_for && exec uwsgi --ini /uwsgi.conf
elif [[ "$1" == "upgrade" ]]
then
    wait_for && exec python manage.py migrate --noinput
elif [[ "$1" == "get_static" ]]
then
    wait_for && exec python manage.py collectstatic --noinput
else
    exec $1
fi
