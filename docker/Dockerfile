# Stage 1: Builder
FROM python:3.11-slim as builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies into a specific folder
COPY requirements.txt pyproject.toml ./
RUN pip install --upgrade pip && \
    pip install --target=/app/dependencies -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY README.md LICENSE ./

# Stage 2: Production
FROM python:3.11-slim as production

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src:/app/dependencies:$PYTHONPATH"

# Create non-root user
RUN groupadd -r dolibarr && useradd -r -g dolibarr dolibarr

WORKDIR /app

# Copy dependencies and source from builder
COPY --from=builder /app/dependencies ./dependencies
COPY --from=builder /app/src ./src

RUN chown -R dolibarr:dolibarr /app

USER dolibarr

EXPOSE 8080

# Launch server
CMD ["python", "-m", "dolibarr_mcp.dolibarr_mcp_server"]
