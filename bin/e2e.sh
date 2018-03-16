#!/usr/bin/env bash

docker stop $(docker ps -a -q) > /dev/null 2>&1
docker rm $(docker ps -a -q) > /dev/null 2>&1
docker network prune -f > /dev/null 2>&1
docker volume prune -f > /dev/null 2>&1

if [ -z "$1" ]; then
    YML="../docker-compose.dev.yml"
else
    YML=$1
fi
if [[ -z "${POOL_SIZE}" ]]; then
    POOL_SIZE=2
fi
if [[ -z "${SHARDS}" ]]; then
    SHARDS=1
fi

docker-compose -p "dev" -f $YML up -d --scale xqa-shard=$SHARDS

docker run -d --net="dev_xqa" --name="dev_xqa-ingest_1" -v $HOME/GIT_REPOS/xqa-test-data:/xml xqa-ingest:latest -message_broker_host xqa-message-broker -path /xml

exit $?
