import os
import psycopg2
import pymongo
import re

from configparser import ConfigParser

from bson import ObjectId
from pymongo.errors import ConnectionFailure
from urllib.parse import quote_plus

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from db_volsu import settings
from db_volsu.configs import params, psql_params
from db_volsu.help_funcs.database_funcs import get_context, get_columns, get_context_by_id
from db_volsu.help_funcs.exceptions import BadConnectionCredentials
from db_volsu.help_funcs.print_funcs import print_success, print_info, print_error


def base_page(request):
    if request.method == "POST":
        key_set = params.CONNECTION_PARAMS
        key_set.add('system')
        cache_data = {key: request.POST[key] for key in key_set}
        if not cache_data:
            return redirect('login_page')

        cache_timeout = settings.CACHE_TTL
        cache.set_many(cache_data, timeout=cache_timeout)

        return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}))

    if cache.get("database") is None:
        parser = ConfigParser()
        parser.read(os.path.join(settings.BASE_DIR, "db_volsu/configs/database_defaults.ini"))

        context = {}
        if parser.has_section(params.DEFAULTS_SECTION_NAME):
            db_params = parser.items(section=params.DEFAULTS_SECTION_NAME)
            context = {parameter[0]: parameter[1] for parameter in db_params}

        return render(request, 'login_page/login_page.html', context=context)

    return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}))


def get_table(request, table_name="bus_depot"):
    connection = None
    try:
        connection = connect_to_db()

        database_system = cache.get('system')
        result = None
        if database_system == "psql":
            row = psql_params.TABLE_LIST.get(table_name)
            if row is not None:
                result = get_context(request, connection, row)

        else:
            result = get_context(request, connection[table_name], mongo=True)

        template_name = f"database_page/{table_name}.html"
        request_context = {
            "table": table_name,
            "template": template_name,
            "result": result
        }

    except (Exception, BadConnectionCredentials, psycopg2.Error) as exception:
        cache.delete_many(["database", "user", "password"])
        print_error(exception)
        return redirect('login_page')

    finally:
        if connection and not connection.closed:
            close_connection(connection)

    return render(request, 'database_page/database.html', context=request_context)


def change_data(request, table_name="bus_depot", row_id=None, operation=None):
    connection = None
    page_number = request.GET.get('page', 1)

    try:
        connection = connect_to_db()

        if row_id is None:
            return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}) + f"?page={page_number}")

        database_system = cache.get('system')
        if database_system == "mongo":
            if operation != "update":
                raise NotImplemented

            data = request.GET.get('data', '').split(',')
            updated = {}
            for values in data:
                temp = re.sub('[\' ]', '', values).split('=')
                updated[temp[0]] = temp[1]

            connection[table_name].update_one({'_id': ObjectId(row_id)}, {'$set': updated})

        else:
            with connection.cursor() as cursor:
                row_template = psql_params.CHANGE_OPERATIONS.get(operation)

                if row_template is not None:
                    format_values = {
                        "table": table_name,
                        "row_id": int(row_id),
                    }

                    if operation == "update":
                        data = request.GET.get('data')
                        format_values["updated"] = data
                    cursor.execute(row_template.format(**format_values))
                    connection.commit()

    except (Exception, BadConnectionCredentials, psycopg2.Error) as exception:
        cache.delete_many(["database", "user", "password"])
        print_error(exception)
        return redirect('login_page')

    finally:
        if connection and not connection.closed:
            close_connection(connection)

    return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}) + f"?page={page_number}")


def update(request, table_name="bus_depot"):
    page_number = request.GET.get('page', 1)
    if request.method == "POST":
        row_id = request.POST.get('row_id')
        data = {key: request.POST[key] for key in request.POST.keys()
                if key != 'row_id' and key != 'csrfmiddlewaretoken'}
        str_data = ", ".join(f"{key} = '{value}'" for key, value in data.items())
        context = {
            'table_name': table_name,
            'row_id': row_id,
            'operation': 'update'
        }

        return redirect(reverse('change_data', kwargs=context) + f"?page={page_number}&data={str_data}")

    row_id = request.GET.get('row_id')
    connection, column_result = None, None
    try:
        connection = connect_to_db()

        database_system = cache.get('system')
        if database_system == "psql":
            column_result = get_columns(connection, table_name)
            _, result = get_context_by_id(connection, table_name, row_id)
        else:
            column_result, result = get_context_by_id(connection[table_name], table_name, row_id, mongo=True)

    except (Exception, BadConnectionCredentials, psycopg2.Error) as exception:
        cache.delete_many(["database", "user", "password"])
        print_error(exception)
        return redirect('login_page')

    finally:
        if connection and not connection.closed:
            close_connection(connection)

    return render(request, 'update_page/update.html', context={"table": table_name,
                                                               'row_id': row_id,
                                                               'columns': column_result,
                                                               'result': result})


def connect_to_db():
    key_set = params.CONNECTION_PARAMS
    con_params = cache.get_many(key_set)
    if not con_params:
        return None

    print_info("Connecting to database")
    try:
        database_system = cache.get('system')
        if database_system == "psql":
            connection = psycopg2.connect(**con_params)
            if connection is None:
                raise ConnectionFailure

        else:
            mongo_uri = params.MONGO_URI.format(user=quote_plus(con_params.get('user')),
                                                password=quote_plus(con_params.get('password')),
                                                host=quote_plus(con_params.get('host')),
                                                database=quote_plus(con_params.get('database')))
            connection = pymongo.MongoClient(mongo_uri)

            # The ismaster command is cheap and does not require auth.
            connection.admin.command('ismaster')
            connection = connection[con_params.get('database')]

    except ConnectionFailure:
        print_error("Bad credentials for database connection")
        raise BadConnectionCredentials

    print_success("Connection was established")
    return connection


def disconnect(request):
    print_info("Disconnecting")
    cache.clear()
    print_success("Connection was closed")
    return redirect('login_page')


def close_connection(connection):
    print_info("Disconnecting from database")
    connection.close()
    print_success("Connection was closed")