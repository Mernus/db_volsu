import os
from configparser import ConfigParser

import psycopg2
from django.core.cache import cache
from django.shortcuts import render, redirect

from db_volsu import settings
from db_volsu.configs import params
from db_volsu.help_funcs.database_funcs import get_context
from db_volsu.help_funcs.print_funcs import print_success, print_info, print_error


def base_page(request):
    if request.method == "POST":
        key_set = settings.CONNECTION_PARAMS
        cache_data = {key: request.POST[key] for key in key_set}

        # TODO: проверить, что есть все данные, в противном случае слать в жопу
        cache_timeout = settings.CACHE_TTL
        cache.set_many(cache_data, timeout=cache_timeout)

        return redirect("/database/")

    if cache.get("host", None) is None:
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
    depos_info = []
    try:
        key_set = settings.CONNECTION_PARAMS
        params = cache.get_many(key_set)
        if not params:
            return redirect("/")

        print_info("Connecting to database")
        connection = psycopg2.connect(**params)
        print_success("Connection was established")

        depos_info = get_context(connection)

    except (Exception, psycopg2.Error) as exception:
        print(exception)

    finally:
        if connection is not None and not connection.closed:
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

    return render(request, 'database.html', context={"depos_info": depos_info})


def update_defaults(request):
    if request.method != "POST":
        print_error("Bad request for update defaults")
        return

    update_data = {key: request.POST[key] for key in ["host", "port"]}
    parser = ConfigParser()

    print_info("Updating defaults parameters")
    ini_file = params.DEFAULTS_INI_FILE_PATH
    parser.read(ini_file)
    print_success("Config readed")

    db_section = params.CONNECTION_SECTION_NAME
    if parser.has_section(db_section):
        for option, value in update_data.items():
            parser.set(db_section, option, value)

        with open(ini_file, "wb") as config_file:
            parser.write(config_file)
        print_success("Default params was updated")
    else:
        print_error("Bad section name for update defaults request")
