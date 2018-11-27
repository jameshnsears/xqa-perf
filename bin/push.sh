#!/usr/bin/env bash

function push_to_docker_hub() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    echo ">>> $(date --rfc-3339='ns') publish_to_docker_hub $1"
    docker tag $1 jameshnsears/$1
    docker push jameshnsears/$1:latest
    docker rmi jameshnsears/$1:latest
}

# one time password request / login
docker login -u jameshnsears

push_to_docker_hub xqa-db
push_to_docker_hub xqa-db-amqp
push_to_docker_hub xqa-ingest
push_to_docker_hub xqa-ingest-balancer
push_to_docker_hub xqa-message-broker
push_to_docker_hub xqa-query-ui
push_to_docker_hub xqa-query-balancer
push_to_docker_hub xqa-shard

docker search jameshnsears

exit $?
