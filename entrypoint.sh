#!/bin/sh

if [ "$DATABASE" = "sqlite" ] && ! [ -f "$DB_PATH" ]
then
    touch "$DB_PATH"
    flask init-db
fi

flask db upgrade

exec "$@"