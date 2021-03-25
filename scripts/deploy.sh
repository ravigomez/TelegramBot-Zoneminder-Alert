#! /bin/bash

git pull
docker-compose build
./scripts/stop.sh 
./scripts/start.sh
echo "Waiting for 8 secounds..."
sleep 8
./scripts/update-permissions.sh
./scripts/install_selenium-crontab.sh