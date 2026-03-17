FROM ghcr.io/astral-sh/uv:debian

WORKDIR /app

COPY pyproject.toml .

RUN uv sync

COPY main.py .

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]