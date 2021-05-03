FROM python:3.8.7-slim-buster
RUN apt-get update && apt-get install -y \
  cron \
  make \
  && rm -rf /var/lib/apt/lists/*
RUN echo "0 0 * * * find /usr/src/app/temp/ -type f -exec rm -f {} +" >> ~/mycron
RUN crontab -u root ~/mycron
RUN rm ~/mycron
RUN service cron start
RUN groupadd -r telegranbot && useradd --no-log-init -r -g telegranbot telegranbot
WORKDIR /usr/src/app
COPY Makefile .
RUN mkdir src
COPY src/requirements.txt ./src
RUN make
COPY src/ ./src
RUN mkdir scripts
COPY scripts/ ./scripts
RUN mkdir localDB
RUN chown -R telegranbot:telegranbot /usr/src/app
VOLUME [ "/usr/src/app/localDB" ]
USER telegranbot
CMD [ "python", "src/bot.py" ]