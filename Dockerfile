FROM python:3.10-slim-buster

# Install only what's needed and clean up to reduce image size
RUN apt-get update -y \
    && apt-get install -y --no-install-recommends awscli \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy only what you need for pip install first (faster caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your app
COPY . .

# Default command
CMD ["python3", "app.py"]
