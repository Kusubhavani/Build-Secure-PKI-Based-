# -------------------------
# Stage 1: Builder
# -------------------------
FROM python:3.11-slim AS builder

WORKDIR /src

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies into a separate prefix
COPY requirements.txt .
RUN python -m pip install --upgrade pip \
    && pip install --prefix=/install -r requirements.txt

# Copy application code
COPY app.py scripts/ /src/

# -------------------------
# Stage 2: Runtime
# -------------------------
FROM python:3.11-slim AS runtime

WORKDIR /app

# Set timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo "UTC" > /etc/timezone

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy application code from builder
COPY --from=builder /src /app

# Copy cron jobs
COPY cron/2fa-cron /etc/cron.d/2fa-cron

# Set permissions
RUN chmod 0644 /etc/cron.d/2fa-cron \
    && mkdir -p /data /cron /app/scripts \
    && chmod -R 755 /data /cron /app/scripts

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Expose port
EXPOSE 8080

# Start container
ENTRYPOINT ["/entrypoint.sh"]
