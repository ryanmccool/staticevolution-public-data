FROM python:3.12-slim
ENV PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python build_database.py
CMD datasette serve staticevolution.db --host 0.0.0.0 --port ${PORT:-8001} --metadata metadata.json --secret ${DATASETTE_SECRET} --immutable staticevolution.db --setting sql_time_limit_ms 15000 --setting allow_download off
