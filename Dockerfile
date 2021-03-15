FROM python:3.8.5-slim-buster
RUN apt-get install ffmpeg -y
WORKDIR /usr/src/app
RUN mkdir localDB
RUN mkdir src
RUN mkdir src/Downloads
RUN mkdir src/videos
COPY .env .
COPY src/requirements.txt ./src
RUN pip install --no-cache-dir -r src/requirements.txt
COPY src/ ./src
CMD [ "python", "src/bot.py" ]
