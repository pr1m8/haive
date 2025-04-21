# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

# ----------------------------
# 1. Install system dependencies
# ----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc python3-dev libpq-dev postgresql-client \
    graphviz pkg-config libcairo2-dev libgirepository1.0-dev \
    libjpeg-dev libopenjp2-7-dev libssl-dev libffi-dev \
    libreoffice poppler-utils tesseract-ocr ffmpeg libsm6 libxext6 \
    libxml2-dev libxslt1-dev git \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# ----------------------------
# 2. Set up Poetry
# ----------------------------
ENV POETRY_VERSION=2.1.2
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install "poetry==$POETRY_VERSION"

# ----------------------------
# 3. Set working directory
# ----------------------------
WORKDIR /app

# ----------------------------
# 4. Copy only dependency declarations (enables Docker layer caching)
# ----------------------------
COPY pyproject.toml poetry.lock* ./
COPY packages/haive-core/pyproject.toml     packages/haive-core/pyproject.toml
COPY packages/haive-agents/pyproject.toml   packages/haive-agents/pyproject.toml
COPY packages/haive-games/pyproject.toml    packages/haive-games/pyproject.toml
COPY packages/haive-dataflow/pyproject.toml packages/haive-dataflow/pyproject.toml
COPY packages/haive-prebuilt/pyproject.toml packages/haive-prebuilt/pyproject.toml
COPY packages/haive-tools/pyproject.toml    packages/haive-tools/pyproject.toml

# ----------------------------
# 5. Install dependencies (cached unless pyproject.toml changes)
# ----------------------------
RUN poetry install --with dev

# ----------------------------
# 6. Copy full package sources and app code
# ----------------------------
COPY packages ./packages
COPY src ./src

# ----------------------------
# 7. Install PyTorch (CPU build by default)
# ----------------------------
ARG TORCH_INDEX_URL=https://download.pytorch.org/whl/cpu
RUN pip install torch==2.6.0 torchvision==0.21.0 torchaudio==2.6.0 \
    --index-url $TORCH_INDEX_URL

# ----------------------------
# 8. Expose port & set command
# ----------------------------
EXPOSE 8000
CMD ["python", "-m", "haive.main"]
