FROM python:3.12-slim

ARG APP_HOME=/app
WORKDIR ${APP_HOME}

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ${APP_HOME}
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

COPY . ${APP_HOME}

# Build the static bundle. WhiteNoise serves it directly, which is why this
# stack needs no nginx container -- the host reverse proxy handles TLS/domain.
# DEBUG=False here so CompressedStaticFilesStorage is used, producing .gz
# alongside each asset.
RUN DEBUG=False python manage.py collectstatic --noinput --clear

# db.sqlite3 ships in the repo with the demo rows; this just applies any
# outstanding Django migrations on top of it.
RUN python manage.py migrate --noinput

EXPOSE 5005
CMD ["gunicorn", "--config", "gunicorn-cfg.py", "config.wsgi"]
