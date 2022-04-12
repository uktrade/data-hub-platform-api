# Data Hub Platform API [![CircleCI](https://circleci.com/gh/uktrade/data-hub-platform-api/tree/main.svg?style=shield)](https://circleci.com/gh/uktrade/data-hub-platform-api/tree/main)

Enables digital teams to build services that intersect with Data Hub.

Right now this code exists to provide a proof of concept.

# Requirements

- Python (version specified in .python-version file)
- Poetry
- Make
- Docker Compose

# Running tests

To run the tests once `make test`

To watch on files for a continuous testing experience `make watch-test`

# Redis

Start redis with `make .redis`
Stop redis with `make stop`

The Makefile starts a redis server with docker-compose, but avoid rerunning docker-compose commands by creating a `.redis` target file.
The target file is deleted when `make stop` is run.

If for any reason the `.redis` file hangs around longer than the redis server stays alive, the tests will not pass. 