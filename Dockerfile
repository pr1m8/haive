# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# System dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set up Poetry
ENV POETRY_VERSION=2.1.2
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# Copy root dependency files
COPY pyproject.toml poetry.lock* ./

# Copy local package sources (assumes they are declared as [tool.poetry.dependencies] or dev dependencies)
COPY packages/haive-core ./packages/haive-core
COPY packages/haive-agents ./packages/haive-agents
COPY packages/haive-games ./packages/haive-games
COPY packages/haive-dataflow ./packages/haive-dataflow
COPY packages/haive-prebuilt ./packages/haive-prebuilt
COPY packages/haive-tools ./packages/haive-tools

# Install Poetry
RUN pip install "poetry==$POETRY_VERSION"

# Install dependencies (assumes packages above are declared as path deps or dev group)
RUN poetry install --with dev --no-root && poetry install --only-root

# Install PyTorch (CPU variant by default)
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url $TORCH_INDEX_URL

# Copy application code
COPY src ./src

EXPOSE 8000

CMD ["python", "-m", "haive.main"]
