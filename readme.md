# cress.space

## Development setup

```
docker-compose build
docker-compose run web reset_db
docker-compose run web migrate
docker-compose run web createsuperuser
docker-compose up -d
```


## Production setup

```
# database
docker run -d --restart=always --name cress-db postgres:9.4

# home
docker run -d --name cress-data -v /home/uid1000 -v /home/cress/data:/home/uid1000/cress aexea/aexea-base

# python/nginx
docker build --tag=cress-prod .
docker rm -f cress
docker run -d --volumes-from cress-data --link cress-db:db -v `pwd`/cress/cress/settings/production.py:/opt/code/cress/cress/settings/production.py --restart=always --name cress cress-prod
docker rm -f cress-nginx
docker run --name cress-nginx --net="host" --volumes-from cress-data -p 80:80 -v `pwd`/nginx.conf:/etc/nginx/nginx.conf --restart=always -d nginx


```

### initial

```
docker exec -ti cress python3 ./manage.py reset_db --settings=cress.settings.production
docker exec -ti cress python3 ./manage.py migrate --settings=cress.settings.production
docker exec -ti cress python3 ./manage.py createsuperuser --settings=cress.settings.production
```