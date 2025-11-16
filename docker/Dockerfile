# -----------------------------------------------------------------------------
# Dockerfile for Single-Cell Atlas Builder
# -----------------------------------------------------------------------------
# This Dockerfile sets up a container for the Single-Cell Atlas Builder API.
# It installs Python 3.10, required system libraries, Python dependencies,
# and exposes the FastAPI server on port 8000.
# -----------------------------------------------------------------------------

# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python requirements first for efficient caching
COPY requirements.txt .

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        python3-dev \
        gcc \
        libxml2-dev \
        libxslt1-dev \
        libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code
COPY . .

# Expose FastAPI default port
EXPOSE 8000

# Default command to run FastAPI using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
