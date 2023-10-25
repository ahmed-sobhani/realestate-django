FROM odoku/geopython:3.6

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

COPY ["Pipfile", "Pipfile.lock", ".build/wait-for.sh", ".build/entrypoint.sh", ".build/uwsgi.conf", "/"]

RUN addgroup -g 1000 www-data && adduser -u 1000 -HD -G www-data www-data && \
    apk add --no-cache --virtual .build-deps \
        libffi-dev && \
    apk add --update --no-cache \
        postgresql-dev \
        pcre-dev \
        supervisor \
        zlib-dev \
        jpeg-dev \
        tzdata && \
    pip install --no-cache-dir pipenv && \
    pipenv install --system --deploy && \
    apk del .build-deps && \
    rm -rf /var/cache/apk/*  && rm -rf /root/.cache && \
    chmod +x /wait-for.sh && chmod +x /entrypoint.sh && \
    mkdir -p /var/www/media && \
    mkdir -p /var/www/static && \
    chown www-data:www-data -R /var/www/media && \
    chown www-data:www-data -R /var/www/static

COPY --chown=www-data:www-data . /var/www

USER www-data

RUN cd /var/www && \
    DJANGO_SETTINGS_MODULE=_core.settings python manage.py collectstatic --no-input

WORKDIR /var/www

# WSGI
EXPOSE 9000

# ASGI
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
