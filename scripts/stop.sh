#! /bin/bash

undeploy(){
    docker stack rm telegram-bot
}

undeploy

if [ $? -gt 0 ]; then
    sleep 2
    undeploy
    if [ $? -gt 0]; then
        echo "Erro while trying to undeploy application. Unable to undeploy, try again."
    fi
fi

echo "Undeploy completed successfully!"