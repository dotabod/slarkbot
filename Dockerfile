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

# Set the entry point or command to run your application
CMD [ "python", "app.py" ]
