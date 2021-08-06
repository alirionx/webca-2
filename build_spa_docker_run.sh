#/bin/bash

TGTDIR=/app/backend/dist

export DEBIAN_FRONTEND=noninteractive
apt update
apt install -y curl
curl -fsSL https://deb.nodesource.com/setup_15.x | bash -

if ! command -v node --version &> /dev/null
then
  apt install -y nodejs
fi

if ! command -v vue --version &> /dev/null
then
  npm install -g @vue/cli
fi

cd /app/spa
npm install
npm run build

#if [ -d "$TGTDIR" ]; then
#  rm -R /app/backend/dist
#fi

cp -R dist/ /tmp/ 