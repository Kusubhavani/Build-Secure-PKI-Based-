# -------------------------------
# Stage 1: Builder
# -------------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (optimizes caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# -------------------------------
# Stage 2: Runtime
# -------------------------------
FROM python:3.12-slim

ENV TZ=UTC
WORKDIR /app

# Install cron, timezone tools, and python3 for cron job
RUN apt-get update && apt-get install -y --no-install-recommends \
    cron \
    tzdata \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone
RUN ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone

# Copy installed Python modules from builder
COPY --from=builder /usr/local/lib/python3.12/ /usr/local/lib/python3.12/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy application code & keys
COPY app /app/app
COPY student_private.pem /app/student_private.pem
COPY student_public.pem /app/student_public.pem
COPY instructor_public.pem /app/instructor_public.pem

# -------------------------------
# Cron Setup
# -------------------------------
RUN mkdir -p /data && \
    mkdir -p /cron && \
    chmod 755 /data /cron

COPY cron/2fa-cron /etc/cron.d/2fa-cron

RUN chmod 0644 /etc/cron.d/2fa-cron
RUN crontab /etc/cron.d/2fa-cron

# -------------------------------
# Expose API port
# -------------------------------
EXPOSE 8080

# -------------------------------
# Start cron + FastAPI app
# -------------------------------
CMD service cron start && \
    uvicorn app.main:app --host 0.0.0.0 --port 8080
