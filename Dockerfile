FROM python:3.6-slim

RUN pip install requests \
        bs4

WORKDIR /app

ADD cron.py /app

CMD ["python", "./cron.py"]
