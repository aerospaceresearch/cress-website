import hashlib
import hmac
import json

from rest_framework import exceptions, status, viewsets
from rest_framework.response import Response

from django.conf import settings
from django.utils import six

from .serializers import AXSerializer


class AXTextCreateViewSet(viewsets.ViewSet):
    serializer_class = AXSerializer

    @staticmethod
    def signature_valid(request, raw_data):
        try:
            secret = settings.AX_WEBHOOK_TOKEN
            signature_header = request.META['HTTP_X_MYAX_SIGNATURE'].replace('sha1=', '')
            signature_content = hmac.new(
                key=secret.encode('utf-8'),
                msg=raw_data,
                digestmod=hashlib.sha1
            ).hexdigest()
        except AttributeError:
            pass
        except KeyError:
            pass
        except Exception:
            raise
        else:
            return bool(signature_header == signature_content)
        return False

    def create(self, request):
        raw_data = request.stream.read()

        if self.signature_valid(request, raw_data):
            try:
                serializer = self.serializer_class(data=json.loads(raw_data.decode('utf-8')))
            except ValueError as exc:
                raise exceptions.ParseError('JSON parse error - %s' % six.text_type(exc))

            if serializer.is_valid():
                from .models import AxText
                obj = AxText.objects.get(pk=serializer.data['uid'])
                obj.response = serializer.data
                obj._text = serializer.data['text_as_html']
                obj.save()
                return Response({'pk': obj.pk}, status=status.HTTP_201_CREATED)
            raise exceptions.ValidationError(serializer.errors)
        raise exceptions.NotAuthenticated()
