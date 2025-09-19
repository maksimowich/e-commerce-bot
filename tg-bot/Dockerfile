FROM python:3.11

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt alembic.ini ./

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

RUN apt-get update && apt-get install -y postgresql-client

COPY migrations migrations/
COPY src src/

RUN mkdir -p /app/logs

COPY init.sql /app/sql/init.sql

CMD alembic upgrade head &&  PGPASSWORD=${POSTGRES__PASSWORD} psql -h ${POSTGRES__HOST} -U ${POSTGRES__USER} -d ${POSTGRES__DATABASE} -f /app/sql/init.sql \
    && python src/main.py | tee /app/logs/tg-bot.log
