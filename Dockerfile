FROM python:3.6-slim

RUN pip install requests bs4

#Install Cron
RUN apt-get update
RUN apt-get -y install cron

WORKDIR /app
COPY check_site.py .
COPY container_entrypoint.sh .

COPY crontab /etc/cron.d/check-site-cron
RUN chmod 0644 /etc/cron.d/check-site-cron
RUN touch /var/log/cron.log

CMD /app/container_entrypoint.sh
