source common.sh

#rm_existing_containers_networks_volumes

if [[ -z "${SHARDS}" ]]; then
    SHARDS=4
fi


echo $SHARDS

# docker-compose -p "dev"  -f ../docker-compose.dev.yml -f ../docker-compose.dev.shard.yml up -d --scale xqa-shard=$SHARDS 
# 
# docker run -d --net="dev_xqa" --name="dev_xqa-ingest_1" -v $HOME/GIT_REPOS/xqa-test-data:/xml xqa-ingest:latest -message_broker_host xqa-message-broker -path /xml
# 
# docker network ls
# docker volume ls
# docker ps -a

exit $?
