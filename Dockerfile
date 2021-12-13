FROM python:3.10.1-alpine3.15

COPY requirements.txt /github-api/requirements.txt

RUN /usr/local/bin/pip install --no-cache-dir --requirement /github-api/requirements.txt

ENV PYTHONUNBUFFERED="1" \
    TZ="Etc/UTC"

ENTRYPOINT ["/usr/local/bin/python"]
