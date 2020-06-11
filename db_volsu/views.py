import os
from configparser import ConfigParser

import psycopg2
from django.core.cache import cache
from django.shortcuts import render, redirect

from db_volsu import settings
from db_volsu.configs import params
from db_volsu.help_funcs.database_funcs import get_context
from db_volsu.help_funcs.exceptions import BadConnectionCredentials
from db_volsu.help_funcs.print_funcs import print_success, print_info, print_error


def base_page(request):
    if request.method == "POST":
        key_set = params.CONNECTION_PARAMS
        print("host " + str(cache.get('host', None)))
        cache_data = {key: request.POST[key] for key in key_set}
        print("cachedata " + str(cache_data))
        if not cache_data:
            return redirect("/")

        # TODO: проверить, что есть все данные, в противном случае слать в жопу
        if cache_data['host'] == "localhost" and cache_data['port'] == "5432":
            cache_data.pop('host')
            cache_data.pop('port')

        print("cachedata " + str(cache_data))
        cache_timeout = settings.CACHE_TTL
        cache.set_many(cache_data, timeout=cache_timeout)

        return redirect("/database/")

    if cache.get("database", None) is None:
        parser = ConfigParser()
        parser.read(os.path.join(settings.BASE_DIR, "db_volsu/configs/database_defaults.ini"))

        dict_params = {}
        if parser.has_section(params.DEFAULTS_SECTION_NAME):
            db_params = parser.items(section=params.DEFAULTS_SECTION_NAME)
            dict_params = {parameter[0]: parameter[1] for parameter in db_params}
        # TODO: проверить, что dict_params объявлен
        return render(request, 'login_page.html', context=dict_params)

    return redirect("/database/")


def database(request):
    connection = None
    try:
        key_set = params.CONNECTION_PARAMS
        con_params = cache.get_many(key_set)
        print("con_params " + str(con_params))
        if not con_params:
            return redirect("/")

        print_info("Connecting to database")
        connection = psycopg2.connect(**con_params)
        if connection is None:
            print_error("Bad credentials for database connection")
            raise BadConnectionCredentials

        print_success("Connection was established")

        depos_info = get_context(connection, params.SCHEDULE_RAW)

    except (BadConnectionCredentials, psycopg2.Error):
        cache.delete_many(["database", "user", "password"])
        return redirect("/")

    finally:
        if not connection.closed:
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

    return render(request, 'database.html', context={"depos_info": depos_info})
