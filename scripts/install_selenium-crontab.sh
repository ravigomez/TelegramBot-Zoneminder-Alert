#! /bin/bash

echo "Looking for the selenium container..."
while :; do
    CONTAINER_ID=$(docker ps | grep telegram-bot_selenium-chrome | fmt -w 1 | head -n1)
    if [ $CONTAINER_ID ]; then
        docker exec -it $CONTAINER_ID sudo apt-get update \
                                      && sudo apt-get install cron -y \
                                      && sudo echo "0 0 * * * find ~/Downloads/ -type f -exec rm -f {} +" >> ~/mycron \
                                      && sudo crontab -u seluser ~/mycron \
                                      && sudo rm ~/mycron
        echo "selenium container found and crontab configured"
        exit 0
    else
        sleep 2
    fi
done

