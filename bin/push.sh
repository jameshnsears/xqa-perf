#!/usr/bin/env bash

source common.sh

function publish_to_docker_hub() {
    echo ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
    NOW=`date --rfc-3339='ns'`
    echo ">>> $NOW publish_to_docker_hub $1"
    docker tag $1 jameshnsears/$1
    docker push jameshnsears/$1:latest
    docker rmi jameshnsears/$1:latest
}

# one time password request / login
docker login -u jameshnsears

publish_to_docker_hub xqa-db
publish_to_docker_hub xqa-db-amqp
publish_to_docker_hub xqa-ingest
publish_to_docker_hub xqa-ingest-balancer
publish_to_docker_hub xqa-message-broker
publish_to_docker_hub xqa-query-ui
publish_to_docker_hub xqa-query-balancer
publish_to_docker_hub xqa-shard

docker search jameshnsears

exit $?
