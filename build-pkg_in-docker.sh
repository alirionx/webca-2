#/bin/bash

#---------------------------
TS=$(date +%s%N)
CONNAME=npmbuild_$TS
NODESRC=https://deb.nodesource.com/setup_16.x
TMPPATH="/home/$USER/tmp/$TS"

#---------------------------
mkdir -p $TMPPATH/webca
cp -R ./webapp/*.py $TMPPATH/webca
cp -R ./webapp/settings.yaml $TMPPATH/webca
cp -R ./webapp/requirements.txt $TMPPATH/webca


#---------------------------

docker run -itd --name $CONNAME node:16
docker cp ./spa $CONNAME:/data

docker exec -it -w /data $CONNAME npm install
docker exec -it -w /data $CONNAME npm run build

docker cp $CONNAME:/data/dist $TMPPATH/webca/

docker kill $CONNAME
docker rm $CONNAME

#---------------------------
tar -czf ./webca.tar.gz -C $TMPPATH .
rm -R $TMPPATH

#---------------------------




