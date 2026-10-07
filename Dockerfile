FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# System dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
        nodejs \
        npm \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY . /app

# Upgrade pip
RUN python -m pip install --upgrade pip setuptools wheel

# Install dependencies
RUN pip install --no-cache-dir -r UB.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start bot
CMD ["python", "main.py"]
