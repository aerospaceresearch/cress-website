def environment(request):
    from django.conf import settings
    debug = getattr(settings, 'DEBUG', True)
    return {
        'production': not debug
    }
