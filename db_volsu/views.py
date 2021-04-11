import psycopg2

from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from db_volsu.configs import psql_params
from db_volsu.configs.params import GET_OPERATIONS
from db_volsu.database_utils import connect_to_db, perform_operation
from db_volsu.help_funcs.database_funcs import get_context, get_columns, get_context_by_id
from db_volsu.help_funcs.exceptions import BadConnectionCredentials
from db_volsu.help_funcs.print_funcs import print_error
from db_volsu.utils import clear_cache, close_connection, get_default_context, update_cache_from_request


def base_page(request):
    if request.method == "POST":
        update_cache_from_request(request)
        return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}))

    if cache.get("database") is None:
        context = get_default_context()
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

    except (BadConnectionCredentials, psycopg2.Error, Exception) as exception:
        clear_cache()
        print_error(exception)
        return redirect('login_page')

    finally:
        close_connection(connection)

    return render(request, 'database_page/database.html', context=request_context)


def change_data(request, table_name="bus_depot", operation=None):
    page_number = request.GET.get('page', 1)
    row_id = request.GET.get('row_id')
    if row_id is None and operation != 'add':
        return redirect(reverse('get_table', kwargs={'table_name': 'bus_depot'}) + f"?page={page_number}")

    if request.method == "POST" or operation in GET_OPERATIONS:
        data = {key: request.POST[key] for key in request.POST.keys()
                if key != 'row_id' and key != 'csrfmiddlewaretoken'}
        perform_operation(data, operation, row_id, table_name)

        return redirect(reverse('get_table', kwargs={'table_name': table_name}) + f"?page={page_number}")

    connection, column_result = None, None
    try:
        connection = connect_to_db()

        database_system = cache.get('system')
        if database_system == "psql":
            column_result = get_columns(connection, table_name)
            _, result = get_context_by_id(connection, table_name, row_id)
        else:
            column_result, result = get_context_by_id(connection[table_name], table_name, row_id, mongo=True)

    except (BadConnectionCredentials, psycopg2.Error, Exception) as exception:
        clear_cache()
        print_error(exception)
        return redirect('login_page')

    finally:
        close_connection(connection)

    return render(request, 'update_page/update.html', context={"table": table_name,
                                                               'row_id': row_id,
                                                               'columns': column_result,
                                                               'result': result,
                                                               'operation': operation})


def disconnect(request):
    clear_cache()
    return redirect('login_page')
