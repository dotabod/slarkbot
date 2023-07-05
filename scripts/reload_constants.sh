cd ./scripts
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD \
    psql -U "$POSTGRES_USER" \
    -h "$POSTGRES_HOST" \
    -p $DATABASE_PORT \
    -v db_name="$POSTGRES_DB" \
    -d "$POSTGRES_DB" \
    -f rebuild_constants.sql

cd ..
./scripts/seed.py
