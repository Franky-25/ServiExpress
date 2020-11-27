#!/bin/bash

NAME="husani"
DJANGODIR=/home/jair/husani/app/
SOCKFILE=/tmp/gunicorn.sock
LOGDIR=${DJANGODIR}logs/gunicorn.log
USER=jair
GROUP=jair
NUM_WORKERS=3
DJANGO_SETTINGS_MODULE=config.production
DJANGO_WSGI_MODULE=config.wsgi

rm -frv $SOCKFILE

echo "Starting $NAME as `whoami`"

cd $DJANGODIR

exec /home/jair/husani/env/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
    --name $NAME \
    --workers $NUM_WORKERS \
    --user=$USER --group=$GROUP \
    --bind=unix:$SOCKFILE \
    --log-level=debug \
    --log-file=$LOGDIR