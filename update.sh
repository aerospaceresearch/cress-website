#!/bin/sh

set -e

git pull
docker build --tag=cress-prod .
docker rm -f cress
docker run -d --volumes-from cress-data --link cress-db:db -v `pwd`/cress/cress/settings/production.py:/opt/code/cress/cress/settings/production.py --restart=always --name cress cress-prod
docker rm -f cress-nginx
docker run --name cress-nginx --net="host" --volumes-from cress-data -p 80:80 -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx

echo "Cleaning up old docker images..."
docker rmi $(docker images | grep "<none>" | awk '{print($3)}')
