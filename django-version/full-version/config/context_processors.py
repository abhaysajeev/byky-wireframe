from django.conf import settings

def my_setting(request):
    return {'MY_SETTING': settings}

def language_code(request):
    return {"LANGUAGE_CODE": request.LANGUAGE_CODE}

def get_cookie(request):
    return {"COOKIES": request.COOKIES}

# Add the 'ENVIRONMENT' setting to the template context
def environment(request):
    return {'ENVIRONMENT': settings.ENVIRONMENT}


def alert_feed(request):
    """The navbar bell's alert pool, on every page.

    The navbar is a site-wide partial, so this rides in as a context processor
    rather than being added to each of the 110+ views. Route names are resolved
    to URLs here so the JS can link straight out without knowing Django's
    URLconf. See apps/byky_core/alerts.py for where the alert types come from.
    """
    from django.urls import NoReverseMatch, reverse

    from apps.byky_core import alerts

    feed = []
    for alert in alerts.feed():
        try:
            url = reverse(alert["route"])
        except NoReverseMatch:
            continue
        feed.append(dict(alert, url=url))
    return {"alert_feed": feed}
