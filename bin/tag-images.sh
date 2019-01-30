#!/usr/bin/env bash

docker tag xqa-query-ui jameshnsears/xqa-query-ui
docker tag xqa-db jameshnsears/xqa-db
docker tag xqa-db-amqp jameshnsears/xqa-db-amqp
docker tag xqa-message-broker jameshnsears/xqa-message-broker
docker tag xqa-shard jameshnsears/xqa-shard
docker tag xqa-ingest jameshnsears/xqa-ingest
docker tag xqa-ingest-balancer jameshnsears/xqa-ingest-balancer
docker tag xqa-query-balancer jameshnsears/xqa-query-balancer

docker images
