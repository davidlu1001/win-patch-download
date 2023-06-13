.PHONY: build clean version

export APP_VERSION ?= $(shell git rev-parse --short HEAD)

version:
	@echo '{"Version": "$(APP_VERSION)"}'

build:
	docker-compose build

run:
	docker-compose up -d

clean:
	docker-compose down --rmi all --volumes --remove-orphans
	docker images -q -f dangling=true -f label=application=win-patch-download | xargs -I ARGS docker rmi -f --no-prune ARGS