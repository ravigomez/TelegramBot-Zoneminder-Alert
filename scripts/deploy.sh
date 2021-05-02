#! /bin/bash

#git pull
./scripts/stop.sh
if [ $? -eq 2 ]; then
    echo "Erro. Try again."
    exit 2
fi

docker-compose build

./scripts/start.sh
if [ $? -eq 2 ]; then
    echo "Erro. Try again."
    exit 2
fi