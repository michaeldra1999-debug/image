FROM python:3.10-slim

# System dependencies for pyvips
RUN apt-get update && apt-get install -y \
    libvips \
    libvips-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
