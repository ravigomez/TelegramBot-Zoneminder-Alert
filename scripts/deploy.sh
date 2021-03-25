#! /bin/bash

git pull
docker-compose build
./scripts/stop.sh
if [ $? -eq 2 ]; then
    echo "Erro. Try again."
    exit 2
fi
./scripts/start.sh
if [ $? -eq 2 ]; then
    echo "Erro. Try again."
    exit 2
fi
echo "Waiting for 8 secounds..."
sleep 8
./scripts/update-permissions.sh
./scripts/install_selenium-crontab.sh