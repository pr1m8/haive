# syntax=docker/dockerfile:1

# Base stage for dependencies
FROM python:3.12-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Python packages directly with pip (bypass Poetry completely)
FROM base as builder

WORKDIR /app

# Copy source code
COPY src ./src
COPY packages/haive-core/src ./packages/haive-core/src
COPY packages/haive-agents/src ./packages/haive-agents/src
COPY packages/haive-games/src ./packages/haive-games/src
COPY packages/haive-dataflow/src ./packages/haive-dataflow/src
COPY packages/haive-prebuilt/src ./packages/haive-prebuilt/src
COPY packages/haive-tools/src ./packages/haive-tools/src

# Install dependencies directly with pip
RUN pip install --no-cache-dir \
    langchain-core==0.3.44 \
    langchain==0.3.20 \
    langchain-community==0.3.20 \
    pydantic==2.10.6 \
    langgraph==0.3.5 \
    matplotlib==3.10.0 \
    pandas==2.2.3 \
    psycopg2==2.9.10 \
    fastapi==0.115.12 \
    uvicorn==0.34.0 \
    torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu

# Set work directory paths
ENV PYTHONPATH=/app

# Expose your app's port
EXPOSE 8000

# Set your app's entrypoint
CMD ["python", "-m", "haive.main"]