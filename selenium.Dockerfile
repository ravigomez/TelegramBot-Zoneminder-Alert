FROM selenium/standalone-chrome:3.141.59
USER root
RUN apt update
RUN apt install cron -y
RUN echo "0 0 * * * find ~/Downloads/ -type f -exec rm -f {} +" >> ~/mycron
RUN crontab -u seluser ~/mycron
RUN rm ~/mycron
USER 1200