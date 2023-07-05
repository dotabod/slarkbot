#!/bin/bash

source .env

CONTAINER_NAME="dotabros"

# Check if the container already exists
if [[ $(docker ps -aq -f name=$CONTAINER_NAME) ]]; then
  # Stop the existing container
  docker stop $CONTAINER_NAME

  # Remove the existing container
  docker rm $CONTAINER_NAME
fi

docker build \
  --build-arg OPEN_DOTA_API_BASE_URL="$OPEN_DOTA_API_BASE_URL" \
  --build-arg LOG_LEVEL="$LOG_LEVEL" \
  --build-arg TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" \
  --build-arg POSTGRES_USER="$POSTGRES_USER" \
  --build-arg POSTGRES_PASSWORD="$POSTGRES_PASSWORD" \
  --build-arg POSTGRES_DB="$POSTGRES_DB" \
  --build-arg POSTGRES_HOST="$POSTGRES_HOST" \
  --build-arg PUDGEBOT_VERSION="$PUDGEBOT_VERSION" \
  -t $CONTAINER_NAME .

docker run -d --name $CONTAINER_NAME $CONTAINER_NAME
