FROM ubuntu:latest
LABEL authors="franco"

ENTRYPOINT ["top", "-b"]

FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m venv /venv && \
    /venv/bin/pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

ENV FLASK_APP=run.py
ENV PATH="/venv/bin:$PATH"

CMD ["/venv/bin/gunicorn", "--workers=4" , "--bind", "0.0.0.0:8080", "app:app"]
