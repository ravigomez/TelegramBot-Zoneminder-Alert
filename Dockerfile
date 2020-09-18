FROM python:3.8.5-slim-buster
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg -y
WORKDIR /usr/src/app
RUN mkdir localDB
RUN mkdir src
RUN mkdir src/Downloads
RUN mkdir src/videos
COPY src/ ./src
RUN pip install --no-cache-dir -r src/requirements.txt
COPY .env .
CMD [ "python", "src/bot.py" ]
