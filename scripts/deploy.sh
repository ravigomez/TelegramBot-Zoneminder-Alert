#! /bin/bash

git pull
docker-compose build
./scripts/stop.sh 
./scripts/start.sh
./scripts/update-permissions.sh
