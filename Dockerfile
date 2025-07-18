
# Dockerfile for LLM Enrichment Project
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy .env if provided (optional, for local dev)
# COPY .env /app/.env

# Expose port if running a web server (optional)
# EXPOSE 8000

# Default command to run FastAPI server
CMD ["uvicorn", "api.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
