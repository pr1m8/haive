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
# === Dependencies Stage: Poetry + Deps ===
###########################################
FROM base AS deps

ENV POETRY_VERSION=2.1.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PATH="/opt/poetry/bin:$PATH"

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

# Copy only dependency files first for better caching
COPY pyproject.toml poetry.lock ./

# Copy only the pyproject.toml files from packages for dependency resolution
RUN mkdir -p packages
COPY packages/*/pyproject.toml packages/
RUN find packages -name "pyproject.toml" -exec dirname {} \; | while read dir; do \
    echo "Found package: $dir"; \
    done

# Install main dependencies
RUN poetry install --no-root --only main --no-interaction

# Install each package's dependencies individually
RUN for pkg in packages/*/pyproject.toml; do \
    if [ -f "$pkg" ]; then \
        pkg_dir=$(dirname "$pkg"); \
        echo "Installing dependencies for $pkg_dir"; \
        cd "$pkg_dir" && \
        if [ -f "poetry.lock" ]; then \
            poetry install --no-root --only main --no-interaction || echo "Failed to install $pkg_dir"; \
        else \
            echo "No poetry.lock in $pkg_dir, skipping"; \
        fi && \
        cd /app; \
    fi; \
    done

# Clean up poetry cache
RUN rm -rf $POETRY_CACHE_DIR

###############################################
# === Runtime Stage: Final Image ===
###############################################
FROM base AS runtime

WORKDIR /app

# Copy Python packages from deps stage
COPY --from=deps /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application files
COPY pyproject.toml poetry.lock ./
COPY packages ./packages
COPY haive ./haive

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
