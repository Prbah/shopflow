# Stage 1: Build dependencies
FROM python:3.15-slim-trixie AS builder

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /install /install
COPY services/product-service/main.py /app/main.py

ENV PYTHONPATH=/install/lib/python3.15/site-packages

EXPOSE 8000

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
