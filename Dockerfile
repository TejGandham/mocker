# Use uv base image with Python 3.13 on Debian Trixie
FROM ghcr.io/astral-sh/uv:python3.13-trixie-slim

# Set the working directory
WORKDIR /app

# Copy dependency files and README (required by pyproject.toml)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies system-wide
RUN uv pip install --system --no-cache fastapi uvicorn httpx pydantic

# Copy the application files
COPY ./app /app

# Expose the port FastAPI will run on
EXPOSE 8001

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]