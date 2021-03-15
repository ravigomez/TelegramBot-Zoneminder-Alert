#! /bin/bash

git pull
docker-compose build
./scripts/stop.sh 
./scripts/start.sh

while :; do
    CONTAINER_ID=$(docker ps | grep jenkins | fmt -w 1 | head -n1)
    if [ $CONTAINER_ID ]; then
        docker exec -it $CONTAINER_ID sudo chown -R seluser:seluser /home/seluser/Downloads
        break;
    else
        sleep 2
    fi
done

