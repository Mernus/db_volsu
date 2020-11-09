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
        cache_data = {key: request.POST[key] for key in key_set}
        if not cache_data:
            return redirect("/")

        if cache_data['host'] == "localhost" and cache_data['port'] == "5432":
            cache_data.pop('host')
            cache_data.pop('port')

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
        return render(request, 'login_page/login_page.html', context=dict_params)

    return redirect("/database/")


def get_table(request):
    connection = None
    try:
        key_set = params.CONNECTION_PARAMS
        con_params = cache.get_many(key_set)
        if not con_params:
            return redirect("/")

        print_info("Connecting to database")

        connection = psycopg2.connect(**con_params)
        if connection is None:
            print_error("Bad credentials for database connection")
            raise BadConnectionCredentials

        print_success("Connection was established")

        table_name = request.GET.get('table_name', "bus_depot")
        row = params.TABLE_LIST[table_name]

        del_id = request.GET.get('del_id', None)
        if del_id:
            with connection.cursor() as cursor:
                cursor.execute(params.DELETE_ROW.format(table=table_name, del_id=del_id))

        result = get_context(request, connection, row)

        template_name = f"database_page/{table_name}.html"
        request_context = {
            "table_name": table_name,
            "template": template_name,
            "result": result
        }

    except (Exception, BadConnectionCredentials, psycopg2.Error) as exception:
        cache.delete_many(["database", "user", "password"])
        print_error(exception)
        return redirect("/")

    finally:
        if connection and not connection.closed:
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

    return render(request, 'database_page/database.html', context=request_context)


def disconnect(request):
    print_info("Disconnecting")
    cache.delete_many(["database", "user", "password"])
    print_success("Connection was closed")
    return redirect("/")
