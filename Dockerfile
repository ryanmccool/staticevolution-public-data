FROM python:3.12-slim

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --require-hashes --requirement requirements.txt
COPY build_database.py metadata.json ./
COPY data ./data
RUN python build_database.py

CMD ["sh", "-c", "datasette serve --host 0.0.0.0 --port ${PORT} --metadata metadata.json --secret ${DATASETTE_SECRET} --immutable staticevolution.db --setting allow_download off --setting allow_facet on --setting sql_time_limit_ms 5000"]
