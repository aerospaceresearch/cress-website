#!/bin/sh

set -e

#git pull
docker build --tag=cress-prod .
docker rm -f cress
docker run -d --volumes-from cress-data --link cress-db:db -v `pwd`/cress/cress/settings/production.py:/opt/code/cress/cress/settings/production.py --restart=always --name cress cress-prod

bash nginx.sh

echo "Cleaning up old docker images..."
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
