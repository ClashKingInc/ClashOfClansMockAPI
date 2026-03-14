FROM python:3.13.7-slim

COPY --from=ghcr.io/astral-sh/uv:0.9.2 /uv /bin/uv
WORKDIR /app
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1
ENV PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . ./

EXPOSE 3000

CMD ["python", "main.py"]
