FROM python:3

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -U -r requirements.txt

COPY duolingo.py .
COPY duo_server.py .
COPY exec.sh .
COPY duo_main.py .

HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS 127.0.0.1:7000/health || exit 1
EXPOSE 7000
CMD sh exec.sh