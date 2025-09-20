FROM python:3.11

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt alembic.ini ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y postgresql-client

COPY migrations migrations/
COPY src src/
COPY photos photos/

RUN mkdir -p /app/logs

COPY init.sql /app/sql/init.sql

CMD alembic upgrade head &&  PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_HOST} -U ${POSTGRES_USER} -d ${POSTGRES_DB} -f /app/sql/init.sql \
    && python src/main.py | tee /app/logs/tg-bot.log
