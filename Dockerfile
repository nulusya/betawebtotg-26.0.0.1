# ---- Stage 1: Build Frontend ----
FROM node:20-alpine AS frontend-builder

WORKDIR /app/client

# Copy package files first for caching
COPY client/package*.json ./
RUN npm install

# Copy source and build
COPY client/ .
RUN npm run build

# ---- Stage 2: Runtime Backend ----
FROM python:3.11-slim

WORKDIR /app/server

# Install system dependencies (for psycopg2/asyncpg if needed)
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY server/ .

# Copy built frontend from previous stage
# IMPORTANT: main.py expects '../client/dist' relative to itself in server/
# So we copy dist to /app/client/dist
COPY --from=frontend-builder /app/client/dist /app/client/dist

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Expose port (Koyeb usually detects 8000 but good to be explicit)
EXPOSE 8000

# Start command
# We run from /app/server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
