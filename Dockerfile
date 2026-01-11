# ✅ Working Dockerfile for Flask + PyVips on Render

FROM python:3.10-slim

# Install libvips (needed for pyvips)
RUN apt-get update && \
    apt-get install -y libvips && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy all files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 10000

# Run app with gunicorn
CMD ["gunicorn", "app:app"]
