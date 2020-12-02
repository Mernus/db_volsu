import os
import psycopg2

from configparser import ConfigParser
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from db_volsu import settings
from db_volsu.configs import params
from db_volsu.help_funcs.database_funcs import get_context, get_columns, get_context_by_id
from db_volsu.help_funcs.exceptions import BadConnectionCredentials
from db_volsu.help_funcs.print_funcs import print_success, print_info, print_error


def base_page(request):
    if request.method == "POST":
        key_set = params.CONNECTION_PARAMS
        cache_data = {key: request.POST[key] for key in key_set}
        if not cache_data:
            return redirect('login_page')

        if cache_data['host'] == "localhost" and cache_data['port'] == "5432":
            cache_data.pop('host')
            cache_data.pop('port')

        cache_timeout = settings.CACHE_TTL
        cache.set_many(cache_data, timeout=cache_timeout)

        return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}))

    if cache.get("database", None) is None:
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
        if connection is None:
            return redirect('login_page')

        row = params.TABLE_LIST.get(table_name)

        if row is not None:
            result = get_context(request, connection, row)

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
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

    return render(request, 'database_page/database.html', context=request_context)


def change_data(request, table_name="bus_depot", row_id=None, operation=None):
    connection = None
    page_number = request.GET.get('page', 1)

    try:
        connection = connect_to_db()
        if connection is None:
            return redirect('login_page')

        if row_id is None:
            return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}) + f"?page={page_number}")

        with connection.cursor() as cursor:
            row_template = params.CHANGE_OPERATIONS.get(operation)

            if row_template is not None:
                format_values = {
                    "table": table_name,
                    "row_id": row_id,
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
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

    return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}) + f"?page={page_number}")


def update(request, table_name="bus_depot"):
    page_number = request.GET.get('page', 1)
    if request.method == "POST":
        row_id = request.POST.get('id')
        data = {key: request.POST[key] for key in request.POST.keys()
                if key != 'id' and key != 'csrfmiddlewaretoken'}
        str_data = ", ".join(f"{key} = '{value}'" for key, value in data.items())
        context = {
            'table_name': 'bus_depot',
            'row_id': row_id,
            'operation': 'update'
        }

        return redirect(reverse('change_data', kwargs=context) + f"?page={page_number}&data={str_data}")

    row_id = request.GET.get('row_id')
    connection, column_result = None, None
    try:
        connection = connect_to_db()
        if connection is None:
            return redirect('login_page')

        column_result = get_columns(connection, table_name)
        result = get_context_by_id(connection, table_name, row_id)

    except (Exception, BadConnectionCredentials, psycopg2.Error) as exception:
        cache.delete_many(["database", "user", "password"])
        print_error(exception)
        return redirect('login_page')

    finally:
        if connection and not connection.closed:
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")

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

    connection = psycopg2.connect(**con_params)
    if connection is None:
        print_error("Bad credentials for database connection")
        raise BadConnectionCredentials

    print_success("Connection was established")
    return connection


def disconnect(request):
    print_info("Disconnecting")
    cache.clear()
    print_success("Connection was closed")
    return redirect('login_page')
