FROM python:3.9

WORKDIR /app

# Install PostgreSQL client library and development files
RUN apt-get update && apt-get install -y libpq-dev

# Copy requirements.txt file to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files
COPY . .

# Set the build arguments for environment variables
ARG OPEN_DOTA_API_BASE_URL
ARG LOG_LEVEL
ARG TELEGRAM_BOT_TOKEN
ARG PUDGEBOT_VERSION
ARG POSTGRES_URL

# Set the environment variables
ENV OPEN_DOTA_API_BASE_URL=$OPEN_DOTA_API_BASE_URL
ENV LOG_LEVEL=$LOG_LEVEL
ENV TELEGRAM_BOT_TOKEN=$TELEGRAM_BOT_TOKEN
ENV PUDGEBOT_VERSION=$PUDGEBOT_VERSION
ENV POSTGRES_URL=$POSTGRES_URL

# Set the entry point or command to run your application
CMD ["python", "main.py"]
