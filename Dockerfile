# syntax=docker/dockerfile:1

########################
# === Base Stage ===
########################
FROM python:3.12-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

###############################
# === Poetry & Dependency Layer ===
###############################
FROM base AS builder

ENV POETRY_VERSION=2.1.2 \
    #POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="$POETRY_HOME/bin:$PATH"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Root project setup (readme etc)
COPY pyproject.toml poetry.lock* README.md ./
COPY packages ./packages

# Avoid trying to install the empty `src/haive`
#RUN poetry config package-mode false

# Install all dependency packages
RUN poetry install --with dev --no-root --no-interaction

##########################
# === Final Runtime ===
##########################
FROM base AS runtime

WORKDIR /app

# Poetry already in /usr/local/bin from builder layer
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12

COPY pyproject.toml poetry.lock* README.md ./
COPY packages ./packages
COPY src ./src

# Optional: install torch manually (or via pyproject if already there)
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url $TORCH_INDEX_URL

EXPOSE 8000
CMD ["python", "-m", "haive.main"]
