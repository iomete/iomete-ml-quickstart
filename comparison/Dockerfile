FROM python:3.12-slim

# 1. Install uv binary from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Set WORKDIR early
# This ensures all subsequent paths (like /opt/venv) are relative to a stable root
WORKDIR /app

# 3. Setup Virtual Environment
RUN uv venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 4. Install Dependencies
COPY requirements.txt .

RUN uv pip install -r requirements.txt