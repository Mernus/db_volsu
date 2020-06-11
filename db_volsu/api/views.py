from django.core.cache import cache
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def update_defaults(request):
    if request.method != "POST":
        print("Bad request for update defaults")
        return HttpResponse("Bad request method")

    update_data = {key: request.POST[key] for key in ["host", "port"]}
    if not update_data:
        print("Bad request for update defaults")
        return HttpResponse("Bad data in request")

    cache.set_many(update_data, timeout=None)

    return HttpResponse("All ok")


@csrf_exempt
def clear_redis(request):
    if request.method != "POST":
        print("Bad request for update defaults")
        return HttpResponse("Bad request method")

    cache.clear()

    return HttpResponse("All ok")
