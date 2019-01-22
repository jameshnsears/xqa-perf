#!/usr/bin/env bash

source common.sh

export BLD_DIR=/tmp/xqa
export HOME_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

function clone_git_repo() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    rm -rf ${BLD_DIR}/$1
    echo ">>> $(date --rfc-3339='ns') clone_git_repo"
    git clone https://github.com/jameshnsears/$1 ${BLD_DIR}/$1
}

function docker_compose_build() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo ">>> $(date --rfc-3339='ns') docker_compose_build $1"
    clone_git_repo $1
    cd ${BLD_DIR}/$1
    docker-compose build
    cd ${HOME_DIR}
}

function mvn_docker_compose_build() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo ">>> $(date --rfc-3339='ns') mvn_docker_compose_build $1"
    clone_git_repo $1
    cd ${BLD_DIR}/$1
    mvn clean compile package -DskipTests
    docker-compose build
    cd ${HOME_DIR}
}

function angular() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo ">>> $(date --rfc-3339='ns') ng $1"
    clone_git_repo $1
    cd ${BLD_DIR}/xqa-query-ui
    npm install
    node_modules/@angular/cli/bin/ng build --prod --build-optimizer
    docker-compose build
    cd ${HOME_DIR}
}

function cadvisor() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo ">>> $(date --rfc-3339='ns') cadvisor"
    docker pull google/cadvisor:latest
}

reset_docker_env

angular xqa-query-ui
cadvisor
docker_compose_build xqa-db
docker_compose_build xqa-db-amqp
docker_compose_build xqa-message-broker
docker_compose_build xqa-shard
mvn_docker_compose_build xqa-ingest
mvn_docker_compose_build xqa-ingest-balancer
mvn_docker_compose_build xqa-query-balancer

docker images
