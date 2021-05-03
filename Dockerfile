FROM python:3.8.7-slim-buster
RUN apt-get update
RUN apt install cron make -y
RUN echo "0 0 * * * find /usr/src/app/temp/ -type f -exec rm -f {} +" >> ~/mycron
RUN crontab -u root ~/mycron
RUN rm ~/mycron
RUN service cron start
WORKDIR /usr/src/app
RUN mkdir src
COPY .env .
COPY src/requirements.txt ./src
RUN make
COPY src/ ./src
RUN mkdir scripts
COPY scripts/ ./scripts
CMD [ "python", "src/bot.py" ]