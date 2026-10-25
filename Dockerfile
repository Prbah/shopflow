# Stage 1: Build dependencies
FROM python:3.13-slim-trixie AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Distroless runtime
FROM gcr.io/distroless/python3-debian13:nonroot

WORKDIR /app

COPY --from=builder /install/lib/python3.13/site-packages /usr/lib/python3.13/site-packages
COPY --chown=65532:65532 services/product-service/main.py /app/main.py

ENV PYTHONPATH=/usr/lib/python3.13/site-packages

EXPOSE 8000

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
