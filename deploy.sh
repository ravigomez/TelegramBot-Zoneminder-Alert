git pull
docker-compose build
./scripts/stop.sh 
./scripts/start.sh
docker exec -it $(docker ps | grep telegram-bot_selenium-chrome | fmt -w 1 | head -n1) sudo chown -R seluser:seluser /home/seluser/Downloads