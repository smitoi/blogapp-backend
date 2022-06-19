build:
	if [ ! -e .env ]; then cp .env.example .env; fi
	docker-compose build --no-cache

up:
	docker-compose up -d

down:
	docker-compose down

flake8:
	flake8 blogapp

ssh:
	docker exec -it blogapp /bin/bash