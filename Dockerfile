FROM python:3.8-slim

# Install Redis
RUN apt-get update && apt-get install -y redis-server

# Copy application files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start Redis and the Flask application
CMD ["bash", "-c", "service redis-server start && python app.py"]
