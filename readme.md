# cress.space

## Development setup

```
docker-compose build
docker-compose run web reset_db
docker-compose run web migrate
docker-compose run web createsuperuser
docker-compose up -d
```
