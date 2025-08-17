FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY scripts/start.sh /app/
RUN chmod +x /app/start.sh

RUN python manage.py collectstatic --noinput

CMD ["/app/start.sh"]
