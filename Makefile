ACTIVATE_VENV = pipenv run
PLATFORM := $(shell uname -s)

.PHONY:
	black-format \
	black-format-check \
	bootstrap \
	cheeseshop \
	flake8 \
	install-precommit \
	isort \
	isort-check \
	migrate \
	nuke-venv \
	run-tests \


black-format:
	@$(ACTIVATE_VENV) black .

black-format-check:
	@$(ACTIVATE_VENV) black . --check -q

bootstrap: nuke-venv cheeseshop install-precommit

cheeseshop:
	@if [ $(PLATFORM) = 'Darwin' ]; then\
		export CFLAGS='-Wno-implicit-function-declaration' && export LANG='en_US.UTF-8' && pipenv install --dev;\
	else\
		pipenv install --dev;\
	fi

flake8:
	@$(ACTIVATE_VENV) flake8 --exclude astromonitor_bot/database/alembic/versions .

install-precommit:
	@$(ACTIVATE_VENV) pre-commit install

isort:
	@$(ACTIVATE_VENV) isort . --tc

isort-check:
	@$(ACTIVATE_VENV) isort . --check-only --tc -q

migrate:
	@$(ACTIVATE_VENV) alembic upgrade head

nuke-venv:
	@pipenv --rm;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 1 ]; then\
		echo Skipping virtualenv removal;\
	fi

run-tests:
	@TESTING=1 $(ACTIVATE_VENV) coverage run -m pytest -s $(EXTRA_ARGS)
	@$(ACTIVATE_VENV) coverage report

start-app: migrate
	@cd astromonitor_bot && $(ACTIVATE_VENV) python bot.py
