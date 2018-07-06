#!/usr/bin/env bash

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
