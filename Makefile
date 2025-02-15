.PHONY: build up down logs psql

DOCKER_COMPOSE = docker-compose -f docker/dev/docker-compose.yml --env-file env/.env.dev
POSTGRES_USER=$(shell grep POSTGRES_USER env/.env.dev | cut -d '=' -f2)
POSTGRES_DB=$(shell grep POSTGRES_DB env/.env.dev | cut -d '=' -f2)
POSTGRES_PORT=$(shell grep POSTGRES_PORT env/.env.dev | cut -d '=' -f2)

build:
	$(DOCKER_COMPOSE) build --no-cache

up:
	$(DOCKER_COMPOSE)  up -d

down:
	$(DOCKER_COMPOSE)  down	-v	

logs:
	$(DOCKER_COMPOSE)  logs -f

psql:
	docker exec -it postgres_dev psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -p $(POSTGRES_PORT)