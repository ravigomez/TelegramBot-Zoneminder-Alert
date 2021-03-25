#! /bin/bash

echo "Looking for the selenium container..."
while :; do
    CONTAINER_ID=$(docker ps | grep telegram-bot_selenium-chrome | fmt -w 1 | head -n1)
    if [ $CONTAINER_ID ]; then
        docker exec -it $CONTAINER_ID sudo apt-get update
        docker exec -it $CONTAINER_ID sudo apt-get install cron
        docker exec -it $CONTAINER_ID sudo echo "0 0 * * * find ~/Downloads/ -type f -exec rm -f {} +" >> ~/mycron
        docker exec -it $CONTAINER_ID sudo crontab -u seluser ~/mycron
        docker exec -it $CONTAINER_ID sudo rm ~/mycron
        echo "selenium container found and crontab configured"
    else
        sleep 2
    fi
done

