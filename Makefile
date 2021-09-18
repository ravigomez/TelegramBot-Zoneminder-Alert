PYTHON_VERSION=3.8.7

all: install

install:
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r src/requirements.txt

install dev:
	pyenv install ${PYTHON_VERSION} -s
	pyenv global ${PYTHON_VERSION}
	python3 -m venv venv
	. venv/bin/activate
	pip3 install -r src/requirements.txt

run:
	./venv/bin/python3 src/bot.py

clean:
	find . -type f -name '*.pyc' -delete

deploy:
	docker-compose build
	./scripts/stop.sh
	./scripts/start.sh