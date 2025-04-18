# syntax=docker/dockerfile:1

FROM python:3.12-slim as base

# System dependencies for your stack
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

ENV POETRY_VERSION=1.8.0
ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# Copy root dependency files first for cache efficiency
COPY pyproject.toml poetry.lock* ./

# Copy all package pyproject.toml and README.md files
COPY packages/haive-core/pyproject.toml packages/haive-core/README.md ./packages/haive-core/
COPY packages/haive-agents/pyproject.toml packages/haive-agents/README.md ./packages/haive-agents/
COPY packages/haive-games/pyproject.toml packages/haive-games/README.md ./packages/haive-games/
COPY packages/haive-dataflow/pyproject.toml packages/haive-dataflow/README.md ./packages/haive-dataflow/
COPY packages/haive-prebuilt/pyproject.toml packages/haive-prebuilt/README.md ./packages/haive-prebuilt/
COPY packages/haive-tools/pyproject.toml packages/haive-tools/README.md ./packages/haive-tools/

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install Python dependencies (main only)
RUN poetry install --only main --without dev \
    && pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 --index-url https://download.pytorch.org/whl/cpu

# Now copy the rest of your source code and package sources
COPY src ./src
COPY packages/haive-core/src ./packages/haive-core/src
COPY packages/haive-agents/src ./packages/haive-agents/src
COPY packages/haive-games/src ./packages/haive-games/src
COPY packages/haive-dataflow/src ./packages/haive-dataflow/src
COPY packages/haive-prebuilt/src ./packages/haive-prebuilt/src
COPY packages/haive-tools/src ./packages/haive-tools/src

# Expose your app's port
EXPOSE 8000

# Set your app's entrypoint
CMD ["python", "-m", "haive.main"]