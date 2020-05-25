from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import render
from django.views.decorators.cache import cache_page

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@cache_page(CACHE_TTL)
def base_page(request):
    if request.method == "GET":
        if request.session.is_empty():
            return render(request, 'login_page.html')

        return render(request, 'database.html')

    key_set = ("host", "database", "user", "password", "port")
    cache_data = {key: request.POST[key] for key in key_set}

    # for element in cache_data.items():
    # cache_client.set(*element)

    return render(request, 'database.html')
