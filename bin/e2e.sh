#!/usr/bin/env bash

source common.sh

reset_container_env

if [ -z "$1" ]; then
    YML="../docker-compose.dev.yml"
else
    YML=$1
fi

if [[ -z "${POOL_SIZE}" ]]; then
    POOL_SIZE=2
fi

if [[ -z "${SHARDS}" ]]; then
    SHARDS=2
fi

if [[ -z "${XQA_TEST_DATA}" ]]; then
    XQA_TEST_DATA=$HOME/GIT_REPOS/xqa-test-data
fi

docker-compose -p "dev" -f $YML up -d --scale xqa-shard=$SHARDS

docker run -d --net="dev_xqa" --name="dev_xqa-ingest_1" -v $XQA_TEST_DATA:/xml xqa-ingest:latest -message_broker_host xqa-message-broker -path /xml

exit $?
