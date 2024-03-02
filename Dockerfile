FROM python:3.8-slim

# Copy application files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 5000

# Start the Flask application
CMD ["python", "app.py"]
