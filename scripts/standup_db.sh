#!/bin/bash

cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD createdb -p $DATABASE_PORT -h "$POSTGRES_HOST" -U "$POSTGRES_USER" "$POSTGRES_DB" -w

PGPASSWORD=$POSTGRES_PASSWORD \
    psql -U "$POSTGRES_USER" \
    -h "$POSTGRES_HOST" \
    -p $DATABASE_PORT \
    -v db_name="$POSTGRES_DB" \
    -d "$POSTGRES_DB" \
    -f create_database.sql
