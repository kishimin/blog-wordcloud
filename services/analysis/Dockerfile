FROM python:3.12.11-slim-bookworm

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /uvx /bin/

# Copy the application into the container.
COPY . /services/analysis

# Install the application dependencies.
WORKDIR /services/analysis
RUN uv sync --frozen --no-cache

# Run the application.
CMD [".venv/bin/fastapi", "run", "main.py", "--port", "80", "--host", "0.0.0.0"]