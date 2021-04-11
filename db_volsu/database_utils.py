from urllib.parse import quote_plus

import psycopg2
import pymongo
from bson import ObjectId
from django.core.cache import cache
from django.shortcuts import redirect
from pymongo.errors import ConnectionFailure

from db_volsu.configs.params import CONNECTION_PARAMS, MONGO_URI, PERMITTED_OPERATIONS
from db_volsu.configs.psql_params import CHANGE_OPERATIONS
from db_volsu.help_funcs.exceptions import BadConnectionCredentials
from db_volsu.help_funcs.print_funcs import print_error, print_info, print_success
from db_volsu.utils import clear_cache, close_connection


def perform_operation(data, operation, row_id, table_name="bus_depot"):
    connection = None
    if operation not in PERMITTED_OPERATIONS:
        raise NotImplemented

    try:
        connection = connect_to_db()

        database_system = cache.get('system')
        if database_system == "mongo":
            object_id = ObjectId(row_id)
            if operation == "delete":
                connection[table_name].delete_one({'_id': object_id})
            else:
                connection[table_name].update_one({'_id': object_id}, {'$set': data})

        else:
            with connection.cursor() as cursor:
                row_template = CHANGE_OPERATIONS.get(operation)

                if row_template is not None:
                    format_values = {
                        "table": table_name,
                        "row_id": int(row_id),
                    }

                    if operation == "update":
                        str_data = ", ".join(f"{key} = '{value}'" for key, value in data.items())
                        format_values["updated"] = str_data

                    cursor.execute(row_template.format(**format_values))
                    connection.commit()

    except (BadConnectionCredentials, psycopg2.Error, Exception) as exception:
        clear_cache()
        print_error(exception)
        return redirect('login_page')

    finally:
        close_connection(connection)


def connect_to_db():
    key_set = CONNECTION_PARAMS
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
            mongo_uri = MONGO_URI.format(user=quote_plus(con_params.get('user')),
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
