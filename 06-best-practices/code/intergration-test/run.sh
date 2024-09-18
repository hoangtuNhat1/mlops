#!/usr/bin/env bash 
cd "$(dirname "$0")"
export LOCAL_TAG=`date +"%Y-%m-%d-%H-%M"`
export LOCAL_IMAGE_NAME="stream-model-flower:${LOCAL_TAG}"
docker build -t ${LOCAL_IMAGE_NAME} ..
docker-compose up -d 
sleep 1 
python test_docker.py
ERROR_CODE=$?
if  [ ${ERROR_CODE} != 0]; then 
     docker-compose logs 
fi
docker-compose down 
exit ${ERROR_CODE}