# === Stage 1: Build environment ===
FROM python:3.11-slim AS builder

# Set working directory
WORKDIR /app

# Install system dependencies (only what’s needed for build)
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy dependency file first for better caching
COPY requirements.txt .

# Install dependencies into a temporary directory
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Copy the rest of the application source
COPY . .

# === Stage 2: Minimal runtime image ===
FROM python:3.11-slim AS final

WORKDIR /app

# Copy installed Python packages from builder stage
COPY --from=builder /install /usr/local

# Copy application source (no .git or cache)
COPY . .

# Expose the app port
EXPOSE 5100

# Run the app
CMD ["python", "app/main.py"]
