# ============================================================
# Base Image
# ============================================================
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim

# ============================================================
# Environment
# ============================================================
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

# ============================================================
# Working Directory
# ============================================================
WORKDIR /app

# ============================================================
# Install Dependencies
# Copy dependency files first to leverage Docker cache
# ============================================================
COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ============================================================
# Create Non-Root User
# ============================================================
RUN useradd --create-home --shell /bin/bash appuser

# ============================================================
# Copy Application
# ============================================================
COPY --chown=appuser:appuser app ./app
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser start.py .
COPY --chown=appuser:appuser README.md .

# ============================================================
# Switch User
# ============================================================
USER appuser

# ============================================================
# Expose Streamlit Port
# ============================================================
EXPOSE 8501

# ============================================================
# Start Application
# ============================================================
CMD ["uv", "run", "streamlit", "run", "main.py", "--server.address=0.0.0.0", "--server.port=8501"]