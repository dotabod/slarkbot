#!/bin/bash

cd ./scripts || exit
source ../.env

# Create the database using the URL
createdb "$POSTGRES_URL" -w

# Run SQL scripts using the URL
psql "$POSTGRES_URL" -f create_database.sql
