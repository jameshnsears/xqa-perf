#!/usr/bin/env bash

if [ -z "$1" ]; then
    export YML="../docker-compose.dev.yml"
else
    export YML=$1
fi

if [[ -z "${POOL_SIZE}" ]]; then
    export POOL_SIZE=2
fi

if [[ -z "${SHARDS}" ]]; then
    export SHARDS=2
fi

if [[ -z "${XQA_TEST_DATA}" ]]; then
    export XQA_TEST_DATA=$HOME/GIT_REPOS/xqa-test-data
fi

printf "POOL_SIZE=%s; SHARDS=%s\n" ${POOL_SIZE} ${SHARDS}

docker-compose -f ${YML} up -d xqa-db
docker-compose -f ${YML} up -d xqa-message-broker
docker-compose -f ${YML} up -d --scale xqa-shard=${SHARDS}

export XQA_TEST_DATA=/tmp/xqa/xqa-test-data

docker run -d --net="xqa" --name="xqa-ingest" -v ${XQA_TEST_DATA}:/xml xqa-ingest:latest -message_broker_host xqa-message-broker -path /xml

exit $?
