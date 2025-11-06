# === Stage 1: Build environment ===
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency files first (cache layer)
COPY requirements.txt .

# Install dependencies into a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy app source for build (linting/tests, optional)
COPY app/ app/
COPY main.py .

# === Stage 2: Minimal runtime image ===
FROM python:3.11-slim AS final

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /install /usr/local

# Copy only necessary application files
COPY app/ app/
COPY main.py .
COPY .env.example .env.example

# Create a non-root user and switch
RUN useradd -m appuser && chown -R appuser /app
USER appuser

# Environment variables for safety
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Expose Flask port
EXPOSE 5100

# Run the application
CMD ["python", "app/main.py"]
