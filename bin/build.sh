#!/usr/bin/env bash

source common.sh

function reset_docker_env() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW reset_docker_env"
    docker stop $(docker ps -a -q) > /dev/null 2>&1
    docker rm $(docker ps -a -q) > /dev/null 2>&1
    docker volume prune -f > /dev/null 2>&1
    docker network prune -f > /dev/null 2>&1
    docker images -q | xargs docker rmi -f . > /dev/null 2>&1
}

function docker_compose_build() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW docker_compose_build $1"
    clone_git_repo $1
    cd $BLD_DIR/$1
    docker-compose -p $DOCKER_ENV build
    cd $HOME_DIR
}

function mvn_docker_compose_build() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW mvn_docker_compose_build $1"
    clone_git_repo $1
    cd $BLD_DIR/$1
    mvn clean compile package -DskipTests
    docker-compose -p $DOCKER_ENV build
    cd $HOME_DIR
}

function angular() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW ng $1"
    clone_git_repo $1
    cd $BLD_DIR/xqa-query-ui
    npm install
    npm install -g @angular/cli
    npm install primeng --save
    npm install @angular/animations --save
    npm install font-awesome --save
    ng build --prod --build-optimizer
    docker-compose -p $DOCKER_ENV build
    cd $HOME_DIR
}

function cadvisor() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW cadvisor"
    docker pull google/cadvisor:latest
}

if [[ -z "${TRAVISCI}" ]]; then
    reset_docker_env
    cadvisor
    docker_compose_build xqa-elk
    docker_compose_build xqa-db
    docker_compose_build xqa-db-amqp
fi

angular xqa-query-ui
mvn_docker_compose_build xqa-ingest
mvn_docker_compose_build xqa-ingest-balancer
mvn_docker_compose_build xqa-query-balancer
docker_compose_build xqa-message-broker
docker_compose_build xqa-shard

exit $?
