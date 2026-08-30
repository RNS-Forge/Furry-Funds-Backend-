FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if any are needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the default port
EXPOSE 10000

# Start FastAPI application using uvicorn, dynamically binding to the port provided by Render (falls back to 10000 if not set)
CMD sh -c "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"
