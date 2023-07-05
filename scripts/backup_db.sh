source ./.env
cd ./scripts || exit

CURRENT_TIME=$(date "+%Y.%m.%d-%H.%M.%S")
BACKUP_DIR=~/sql_backups

mkdir $BACKUP_DIR

echo "Creating pg_dump of $POSTGRES_DB"
PGPASSWORD=$POSTGRES_PASSWORD \
  pg_dump "$POSTGRES_DB" \
  -U "$POSTGRES_USER" \
  -p $DATABASE_PORT \
  -h "$POSTGRES_HOST" \
  >$BACKUP_DIR/"$POSTGRES_DB"-"$CURRENT_TIME".backup.sql

echo "backup complete!"
