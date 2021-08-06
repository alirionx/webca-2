#!/bin/bash

TS=$(date +%s)
CONTAINERNAME="spa_build_"$TS
APPDIR="/app"
WORKDIR="/app/spa"

if ! type "docker" > /dev/null; then
  echo "Please install docker befor running this script"
  exit
fi

docker run -itd --name $CONTAINERNAME -w $WORKDIR node:16
docker cp ./spa $CONTAINERNAME:$APPDIR
docker exec $CONTAINERNAME npm install
docker exec $CONTAINERNAME npm run build

rm -R ./webapp/dist/*
docker cp $CONTAINERNAME:$WORKDIR/dist ./webapp/

docker kill $CONTAINERNAME
docker rm $CONTAINERNAME
