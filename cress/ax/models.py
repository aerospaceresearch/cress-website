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
        return f"{self.created}"

    def order_text(self):
        data = {
            "refresh_token": settings.AX_REFRESH_TOKEN
        }
        r = requests.post("https://api.ax-semantics.com/v3/token-exchange/", json=data)
        access_token = r.json()['id_token']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + access_token
        }
        collection_id = settings.AX_COLLECTION_ID
        r = requests.post(f"https://api.ax-semantics.com/v3/collections/{collection_id}/document/", headers=headers, json=self.data_sent)
        assert r.status_code == 201


class AxTiming(TimeStampedModel):
    axtext = models.ForeignKey(AxText, on_delete=models.PROTECT)
    axite_id = models.UUIDField()
    full_generation_roundtrip = models.BigIntegerField()
    return_code = models.IntegerField(null=True, blank=True)

    _access_token = None

    def __str__(self):
        return f"{self.created} {self.return_code}"

    @property
    def access_token(self):
        if not self._access_token:
            data = {
                "refresh_token": settings.AX_REFRESH_TOKEN
            }
            r = requests.post("https://api.ax-semantics.com/v3/token-exchange/", json=data)
            self._access_token = r.json()['id_token']

        return self._access_token

    def push_to_api(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + self.access_token
        }
        data = {
            'axite_id': str(self.axite_id),
            'timing_type': 'full_generation_roundtrip',
            'timing_value': self.full_generation_roundtrip,
        }
        r = requests.post(f"https://api.ax-semantics.com/v3/generation-timing/", headers=headers, json=data)
        self.return_code = r.status_code
        self.save(update_fields=['return_code'])
