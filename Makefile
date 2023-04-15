dev:
	poetry run flask --debug --app page_analyzer:app run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

selfcheck:
	poetry check

lint:
	poetry run flake8 page_analyzer

check: selfcheck lint

install:
	poetry build
	poetry install

setup:
	sh setup.sh

.PHONY: lint selfcheck check install setup
