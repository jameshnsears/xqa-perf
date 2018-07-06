#!/usr/bin/env bash

############################## source common.sh

export BLD_DIR=/tmp/xqa
export HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export DOCKER_ENV="dev"
export POSTGRESQL_VERSION=postgres:10.1

function create_network() {
    docker network create xqa
}

function create_build_dir() {
    if [ -d "$BLD_DIR/$1" ]; then
        rm -rf ${BLD_DIR}/$1
    fi
    mkdir ${BLD_DIR}
}

function clone_git_repo() {
    create_build_dir $1
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW clone_git_repo"
    git clone https://github.com/jameshnsears/$1 ${BLD_DIR}/$1
}

function reset_container_env() {
    docker stop $(docker ps -a -q) > /dev/null 2>&1
    docker rm $(docker ps -a -q) > /dev/null 2>&1
    docker network prune -f > /dev/null 2>&1
    docker volume prune -f > /dev/null 2>&1
}

##############################

reset_container_env

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

docker-compose -p "dev" -f ${YML} up -d xqa-db
docker-compose -p "dev" -f ${YML} up -d xqa-message-broker
docker-compose -p "dev" -f ${YML} up -d --scale xqa-shard=${SHARDS}

docker run -d --net="dev_xqa" --name="dev_xqa-ingest_1" -v ${XQA_TEST_DATA}:/xml xqa-ingest:latest -message_broker_host xqa-message-broker -path /xml

exit $?
