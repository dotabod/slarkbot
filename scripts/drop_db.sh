cd ./scripts || exit
source ../.env

PGPASSWORD=$POSTGRES_PASSWORD dropdb -p $DATABASE_PORT -U "$POSTGRES_USER" -h "$POSTGRES_HOST" "$POSTGRES_DB"
