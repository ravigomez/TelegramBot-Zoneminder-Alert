FROM python:3.8.7-slim-buster
RUN apt-get update
RUN apt install cron -y
RUN echo "0 0 * * * find /usr/src/app/temp/ -type f -exec rm -f {} +" >> ~/mycron
RUN crontab -u root ~/mycron
RUN rm ~/mycron
WORKDIR /usr/src/app
RUN mkdir src
COPY .env .
COPY src/requirements.txt ./src
RUN pip install --no-cache-dir -r src/requirements.txt
COPY src/ ./src
RUN mkdir scripts
COPY scripts/ ./scripts
CMD [ "python", "src/bot.py" ]