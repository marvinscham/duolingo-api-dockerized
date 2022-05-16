FROM python:3

COPY . /

RUN \
pip install --no-cache-dir -U -r requirements.txt

EXPOSE 7000
CMD python3 -m duo_main.py
