#!/usr/bin/env bash

docker pull jameshnsears/xqa-db
docker pull jameshnsears/xqa-db-amqp
docker pull jameshnsears/xqa-db-rest
# docker pull jameshnsears/xqa-elk-elasticsearch
# docker pull jameshnsears/xqa-elk-kibana
# docker pull jameshnsears/xqa-elk-logstash
docker pull jameshnsears/xqa-ingest
docker pull jameshnsears/xqa-ingest-balancer
docker pull jameshnsears/xqa-message-broker
docker pull jameshnsears/xqa-message-broker-filebeat
docker pull jameshnsears/xqa-query-ui
docker pull jameshnsears/xqa-shard

docker images
