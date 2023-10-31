#! /bin/bash

undeploy(){
    docker stack rm telegram-bot
}

undeploy

if [ $? -gt 0 ]; then
    sleep 5
    undeploy
    if [ $? -gt 0 ]; then
        echo "Erro while trying to undeploy application. Unable to undeploy, try again."
        exit 2
    fi
fi

echo "Undeploy completed successfully!"