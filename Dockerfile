FROM python:3-alpine

WORKDIR /app

COPY requirements.txt duolingo.py duo_server.py exec.sh duo_main.py ./

RUN apk add --no-cache --virtual .build-deps gcc musl-dev shadow && \ 
    pip install --no-cache-dir -U -r requirements.txt && \
    apk del .build-deps && \
    adduser -D duolingoapi && \
    chown -R duolingoapi:duolingoapi /app

USER duolingoapi

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS 127.0.0.1:7000/health || exit 1
EXPOSE 7000
CMD sh exec.sh
