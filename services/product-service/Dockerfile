# Stage 1: Install dependencies
FROM python:3.15-slim-trixie AS builder

WORKDIR /install

COPY services/product-service/requirements.txt requirements.txt

RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /install /install
COPY services/product-service/app/ /app/app/

ENV PYTHONPATH=/install/lib/python3.15/site-packages

EXPOSE 8000

CMD ["-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
