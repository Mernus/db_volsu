from django.shortcuts import render


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
