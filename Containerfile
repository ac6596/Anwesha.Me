FROM python:3.11-slim

# Set working directory
WORKDIR /usr/src/app

# Copy dependency definition
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Cloud Run injects the PORT env var (defaults to 8080 locally if unset)
ENV PORT=8080

# Expose port (optional, mostly for local dev reference)
EXPOSE $PORT

# Start Gunicorn server binding to 0.0.0.0 and using the injected PORT
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 main:app
