#!/bin/bash
# push timings
docker run --volumes-from cress-data --link cress-db:db -v /home/cress/cress-website/cress/cress/settings/production.py:/opt/code/cress/cress/settings/production.py --rm --entrypoint /usr/local/bin/python3 --name cress-cron-A cress-prod manage.py push_timings --settings cress.settings.production

# generate texts
docker run --volumes-from cress-data --link cress-db:db -v /home/cress/cress-website/cress/cress/settings/production.py:/opt/code/cress/cress/settings/production.py --rm --entrypoint /usr/local/bin/python3 --name cress-cron-B cress-prod manage.py trigger_text_generation --settings cress.settings.production
