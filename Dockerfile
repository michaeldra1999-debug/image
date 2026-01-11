# ==========================
# ✅ Working Dockerfile for Flask + pyvips on Render
# ==========================

# Base image
FROM python:3.10-slim

# Install libvips (required for pyvips)
RUN apt-get update && \
    apt-get install -y libvips && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy all project files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Start the app with gunicorn (as Render expects)
CMD ["gunicorn", "app:app"]
