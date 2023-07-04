# Use the official Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code into the container
COPY . .

# Set the build arguments for environment variables
ARG OPEN_DOTA_API_BASE_URL
ARG LOG_LEVEL
ARG TELEGRAM_BOT_TOKEN
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB
ARG SLARKBOT_VERSION

# Set the environment variables
ENV OPEN_DOTA_API_BASE_URL=$OPEN_DOTA_API_BASE_URL
ENV LOG_LEVEL=$LOG_LEVEL
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV POSTGRES_USER=$POSTGRES_USER
ENV POSTGRES_PASSWORD=$POSTGRES_PASSWORD
ENV POSTGRES_DB=$POSTGRES_DB
ENV SLARKBOT_VERSION=$SLARKBOT_VERSION

# Run the application
CMD ["python", "main.py"]
