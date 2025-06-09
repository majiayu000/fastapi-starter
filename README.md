# fastapi-starter
A starter project for fastApi

## Development Setup

### Option 1: Using uv (Recommended for production)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv sync

# Run the application
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers
```

### Option 2: Using Poetry (Development)
```bash
# Install dependencies
poetry install

# Run the application
poetry run uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 --proxy-headers
```

## Development Tools (using uvx)

uvx allows you to run development tools without installing them globally:

### Code Quality
```bash
# Format code
uvx black .

# Sort imports
uvx isort .

# Lint and fix code
uvx ruff check . --fix

# Type checking
uvx mypy .

# Security scanning
uvx bandit -r .

# Dependency security check
uvx safety check
```

### Testing and Documentation
```bash
# Run tests
uvx pytest

# Generate test coverage
uvx coverage run -m pytest
uvx coverage html

# Serve documentation
uvx mkdocs serve

# API documentation
uvx pydoc-markdown
```

### Database and Migration
```bash
# Database migrations
uvx alembic init alembic
uvx alembic revision --autogenerate -m "Initial migration"
uvx alembic upgrade head
```

## Production Deployment

For production environments, **uv is highly recommended** due to:
- 10-100x faster dependency resolution and installation
- Smaller memory footprint
- Faster container builds
- Better performance overall

### Docker with uv
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-cache
COPY . .
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```