#! /bin/bash

deploy(){
    docker stack deploy --compose-file docker-compose.yml telegram-bot
}

deploy

if [ $? -gt 0 ]; then
    sleep 5
    deploy
    if [ $? -gt 0 ]; then
        echo "Erro while trying to deploy application. Unable to deploy, try again."
        exit 2
    fi
fi

echo "Deploy completed successfully!"