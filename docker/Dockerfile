# syntax=docker/dockerfile:1

###########################################
# === Base Stage: Python + System Deps ===
###########################################
FROM python:3.12-slim AS base

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🛡️ Add non-root user
RUN useradd -m haiveuser

###########################################
# === Builder Stage: Poetry Install & Deps
###########################################
FROM base AS builder

# Set up Poetry environment
ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy core project metadata and packages
COPY pyproject.toml poetry.lock* README.md ./  
COPY packages ./packages

RUN poetry install --with dev --no-root --no-interaction

###############################################
# === Final Runtime: Clean, Lean App Layer ===
###############################################
FROM base AS runtime

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY pyproject.toml poetry.lock* README.md ./  
COPY packages ./packages
COPY src ./src

# Install torch (optionally skip if included in pyproject already)
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url $TORCH_INDEX_URL

# 🛡️ Switch to non-root user
USER haiveuser

EXPOSE 8000

# ✅ Add HEALTHCHECK to validate the app is alive
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

CMD ["python", "-m", "haive.main"]
