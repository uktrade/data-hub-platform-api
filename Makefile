EXECUTABLES = poetry docker-compose
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

TEST_COMMAND = poetry run pytest -vvv $(TARGET) || (scripts/test_failure.sh $$?)

.PHONY: test stop

.redis:
	@touch .redis
	@docker-compose up -d
	@echo -e "\033[0;35mStarting a redis instance, use make stop to stop it.\033[0m"
	@echo -e "\033[0;35m(We create a temporary .redis file in the project root to save a call to docker-compose every time we run tests.)\033[0m"

test: .redis
	$(TEST_COMMAND)

watch-test:
	@make test --silent || exit 0
	@poetry run watchmedo shell-command --patterns="*.py" --recursive --drop --command="make test --silent" .

stop:
	@echo -e "\033[0;35mStopping Redis...\033[0m"
	@docker-compose down
	@echo -e "\033[0;35mRemoving temporary file...\033[0m"
	unlink .redis

install:
	poetry install