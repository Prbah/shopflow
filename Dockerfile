FROM python:3.13-slim

WORKDIR /app

# Update OS packages available from the configured Debian repositories
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt \
    && python -m pip install --no-cache-dir --upgrade \
       "msgpack>=1.2.1" \
       "setuptools>=78.1.1" \
       "urllib3>=2.8.0" \
    && python -m pip check      

RUN useradd --create-home appuser

COPY --chown=appuser:appuser services/product-service/main.py /app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
