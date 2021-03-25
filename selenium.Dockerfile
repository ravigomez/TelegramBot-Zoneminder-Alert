FROM selenium/standalone-chrome:3.141.59
USER root
RUN apt update
RUN apt install cron -y
USER 1200