FROM python:3.12-slim

# The sandbox drops privileges to an unprivileged uid and, where the host
# permits it, unshares a network namespace. `unshare` comes from util-linux.
RUN apt-get update \
    && apt-get install -y --no-install-recommends util-linux libpq5 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
