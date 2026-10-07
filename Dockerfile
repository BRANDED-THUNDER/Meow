FROM python:3.10-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install FFmpeg and required system packages
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ffmpeg \
        git \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app

# Upgrade pip tools
RUN python -m pip install --upgrade pip setuptools wheel

# Install project dependencies
RUN pip install --no-cache-dir -r UB.txt
RUN pip install --no-cache-dir -r requirements.txt

# Start bot
CMD ["python", "main.py"]
