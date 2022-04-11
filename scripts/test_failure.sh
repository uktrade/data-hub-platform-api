#/bin/env bash

REDIS_HOST="${REDIS_HOST:-localhost}"
REDIS_PORT="${REDIS_PORT:-6379}"

nc -z $REDIS_HOST $REDIS_PORT;
if [ $? != 0 ] && [ ! -f ../.redis ]
then
    echo -e "\n\n\033[0;31mRedis does not appear to be running, but the ./.redis file exists. Run \`make stop\` to fix this \033[0m"
    echo -e "\033[0;35mDid you manually run \`docker-compose stop\` or restart your machine?\033[0m"
fi

exit $1