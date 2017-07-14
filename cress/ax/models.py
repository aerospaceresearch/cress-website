import requests

from django.db import models
from django.conf import settings
from django_extensions.db.models import TimeStampedModel
from django.contrib.postgres.fields import JSONField


class AxText(TimeStampedModel):
    data_sent = JSONField(default=dict)
    response = JSONField(default=dict)
    _text = models.TextField(default='')

    def __str__(self):
        return "{s.created}".format(s=self)

    def order_text(self):
        data = {
            "refresh_token": settings.AX_REFRESH_TOKEN
        }
        r = requests.post("https://idm.ax-semantics.com/v1/token-exchange/", json=data)
        access_token = r.json()['id_token']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + access_token
        }
        collection_id = settings.AX_COLLECTION_ID
        r = requests.post(f"https://api.ax-semantics.com/v2/collections/{collection_id}/document/", headers=headers, json=self.data_sent)
        assert r.status_code == 201
