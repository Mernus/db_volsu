from configparser import ConfigParser

from django.core.cache import cache
from django.shortcuts import render

from db_volsu import settings
from db_volsu.configs import params


def base_page(request):
    if request.method == "POST":
        key_set = settings.CONNECTION_PARAMS
        cache_data = {key: request.POST[key] for key in key_set}

        # TODO: проверить, что есть все данные, в противном случае слать в жопу
        cache_timeout = settings.CACHE_TTL
        cache.set_many(cache_data, timeout=cache_timeout)

        return render(request, 'database.html')

    if cache.get("host", None) is None:
        parser = ConfigParser()
        parser.read(params.DEFAULTS_INI_FILE_PATH)

        if parser.has_section(params.DEFAULTS_SECTION_NAME):
            db_params = parser.items(section=params.DEFAULTS_SECTION_NAME)
            dict_params = {parameter[0]: parameter[1] for parameter in db_params}
        # TODO: проверить, что dict_params объявлен
        return render(request, 'login_page.html', context=dict_params)

    return render(request, 'database.html')
