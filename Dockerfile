FROM python:3-alpine

WORKDIR /app

COPY requirements.txt duolingo.py duo_server.py entrypoint.sh duo_main.py ./

RUN apk add --no-cache --virtual .build-deps gcc musl-dev shadow && \ 
    pip install --no-cache-dir -U -r requirements.txt && \
    apk del .build-deps && \
    adduser -D duolingoapi && \
    touch duo_server.log && \
    chown -R duolingoapi:duolingoapi /app

USER duolingoapi

HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=10s CMD wget -q --spider 127.0.0.1:7000/health || exit 1
EXPOSE 7000
CMD sh entrypoint.sh
