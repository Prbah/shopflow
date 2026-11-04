# Stage 1: Install dependencies
FROM python:3.15-slim-trixie AS builder

WORKDIR /install

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Stage 2: Minimal runtime image
FROM cgr.dev/chainguard/python:latest

WORKDIR /app

COPY --from=builder /install /install
COPY app/main.py /app/main.py

ENV PYTHONPATH=/install/lib/python3.15/site-packages
ENV PYTHONUNBUFFERED=1

EXPOSE 8003

CMD ["-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003"]
