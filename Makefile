build:
	if [ ! -e .env ]; then cp .env.example .env; fi
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

flake8:
	docker exec -it blogapp flake8 blog blogapp

ssh:
	docker exec -it blogapp /bin/bash

test:
	docker exec -it blogapp python3 manage.py test
