#! /bin/bash

git pull
docker-compose build
./scripts/stop.sh 
./scripts/start.sh

echo "Waiting for 10 secounds..."
sleep 10
echo "Looking for the selenium container..."
while :; do
    CONTAINER_ID=$(docker ps | grep telegram-bot_selenium-chrome | fmt -w 1 | head -n1)
    if [ $CONTAINER_ID ]; then
        docker exec -it $CONTAINER_ID sudo chown -R seluser:seluser /home/seluser/Downloads
        echo "selenium container found and permission applied"
        break;
    else
        sleep 2
    fi
done

