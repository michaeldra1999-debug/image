FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y libvips libvips-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .        # 👈 THIS LINE IS MUST

EXPOSE 10000

CMD ["gunicorn", "app:app"]
