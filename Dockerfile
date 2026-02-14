# Music Theory Engine - Dockerfile
# A comprehensive music theory analysis engine for guitarists and musicians

FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies for audio libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libportaudio2 \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy pyproject.toml and requirements first for better caching
COPY music_engine/pyproject.toml /app/pyproject.toml

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy the rest of the application
COPY music_engine/ /app/music_engine/
COPY README.md /app/README.md
COPY LICENSE /app/LICENSE

# Create scripts directory
RUN mkdir -p /app/scripts

# Set default command
CMD ["python", "-m", "music_engine.cli", "--help"]

# Alias for the CLI
RUN echo '#!/bin/bash\npython -m music_engine.cli "$@"' > /usr/local/bin/music-engine && chmod +x /usr/local/bin/music-engine

