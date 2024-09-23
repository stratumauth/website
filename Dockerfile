FROM python:3.12-alpine
LABEL org.opencontainers.image.source=https://github.com/jamie-mh/StratumWebsite

RUN python -m venv /venv
COPY ./requirements.txt /venv/requirements.txt
RUN /venv/bin/pip install --no-cache-dir --upgrade -r /venv/requirements.txt

COPY ./stratum /app/stratum
WORKDIR /app

CMD ["/venv/bin/gunicorn", "--conf", "stratum/gunicorn_conf.py", "--bind", "0.0.0.0:8000", "stratum:create_app()"]
