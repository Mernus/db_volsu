from django.shortcuts import render


def base_page(request):
    if request.method == "GET":
        if request.session.is_empty():
            return render(request, 'login_page.html')

        return render(request, 'database.html')

    key_set = ("host", "database", "user", "password", "port")
    session_data = {key: request.POST[key] for key in key_set}

    session_cache = request.session._session_cache;

    for element in session_data.items():
        session_cache[element[0]] = element[1]

    return render(request, 'database.html')
