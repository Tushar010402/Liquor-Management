FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY src/purchase_service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY src/purchase_service/ .

# Create logs directory
RUN mkdir -p logs

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "purchase_service.wsgi:application"]
