FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip uninstall -y setuptools \
    && pip install --no-cache-dir setuptools==69.1.0 wheel \
    && python -c "import pkg_resources; print('pkg_resources is available')" \
    && pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Make entrypoint script executable
RUN chmod +x /app/docker-entrypoint.sh

# Default command (can be overridden)
CMD ["/app/docker-entrypoint.sh"] 