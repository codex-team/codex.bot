all: help

help:
	@echo "build -------------- - docker compose build."
	@echo "up ----------------- - docker compose up."
	@echo "  clean-py --------- - Remove .pyc/__pycache__ files."
	@echo "restart ------------ - docker compose down & up."
	@echo "i18n --------------- - Generate LC files."
	@echo "	 clean-mo --------- - Remove .mo files."

clean-py:
	-find . -type f -a \( -name "*.pyc" -o -name "*$$py.class" \) | xargs rm
	-find . -type d -name "__pycache__" | xargs rm -r

up: clean-py i18n/ru/LC_MESSAGES/appmanager.mo i18n/ru/LC_MESSAGES/main.mo
	docker-compose up -d

build: clean-py
	docker-compose build

restart: clean-py
	docker-compose down
	docker-compose up -d

clean-mo:
	-find . -type f -a \( -name "*.mo" \) | xargs rm

i18n: clean-mo
	bash ./build_i18n.sh