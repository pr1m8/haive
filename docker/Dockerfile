# syntax=docker/dockerfile:1.7

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
    libxml2-dev libxslt1-dev git curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# 🛡️ Add non-root user
RUN useradd -m haiveuser

###########################################
# === Builder Stage: Poetry Install & Deps
###########################################
FROM base AS builder

ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/opt/poetry/bin:$PATH"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy root files for context/debug
COPY pyproject.toml poetry.lock README.md ./

# Copy all packages — needed before per-package install
COPY packages ./packages

# ✅ DEBUG: Show package structure
RUN echo "📂 Contents of packages/:" && tree -L 2 packages || true

# 🔁 Loop install per package (safe)
RUN set -ex && for d in packages/haive-*; do \
    echo "🔧 Installing $d" && \
    if [ -d "$d" ]; then \
    cd "$d" && \
    poetry install --no-root --only main --no-interaction && \
    cd -; \
    else \
    echo "⚠️  Skipping $d (not a directory)"; \
    fi; \
    done

###############################################
# === Final Runtime Stage: Clean & Minimal ===
###############################################
FROM base AS runtime

WORKDIR /app

# Copy Python site-packages
COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12

# Copy source
COPY pyproject.toml poetry.lock README.md ./
COPY packages ./packages
COPY src ./src

# ⚡ Optional: Torch (skip if bundled in Poetry deps)
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url $TORCH_INDEX_URL

# 🛡️ Non-root user
USER haiveuser

EXPOSE 8000

# ✅ Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8000/health || exit 1

CMD ["python", "-m", "haive.main"]
