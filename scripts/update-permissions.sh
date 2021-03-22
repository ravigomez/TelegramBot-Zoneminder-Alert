#! /bin/bash

echo "Looking for the selenium container..."
while :; do
    CONTAINER_ID=$(docker ps | grep telegram-bot_selenium-chrome | fmt -w 1 | head -n1)
    if [ $CONTAINER_ID ]; then
        docker exec -it $CONTAINER_ID sudo chown -R seluser:seluser /home/seluser/Downloads
        if [ $? -eq 0 ]; then
          echo "selenium container found and permission applied"
        else
          echo "ERRO: the permisions has falid"
          exit 1;
        fi
        exit 0;
    else
        sleep 2
    fi
done

