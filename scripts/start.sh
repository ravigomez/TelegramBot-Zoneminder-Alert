<<<<<<< HEAD
docker stack deploy --compose-file docker-compose.yml telegram-bot
=======
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
>>>>>>> 675e88a9fe0f94d9703c4bbb91478c7cc6f777fe
