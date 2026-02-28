FROM ghcr.io/astral-sh/uv:python3.14-alpine AS python-build

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD pyproject.toml /app/pyproject.toml
ADD uv.lock /app/uv.lock

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:3.14-alpine
LABEL org.opencontainers.image.source=https://github.com/stratumauth/website

COPY ./stratum /app/stratum
COPY --from=python-build /app/.venv /app/.venv

WORKDIR /app

CMD ["/app/.venv/bin/gunicorn", "--conf", "stratum/gunicorn_conf.py", "--bind", "0.0.0.0:8000", "stratum:create_app()"]
