from collections import namedtuple
from configparser import ConfigParser

import psycopg2
from django.core.cache import cache

from db_volsu import settings
from db_volsu.configs import params
from db_volsu.help_funcs.exceptions import BadSectionName
from db_volsu.help_funcs.print_funcs import print_success, print_info


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_context(connection):
    with connection.cursor() as cursor:
        sql_raw = "SELECT bus_schema.bus.id, bus_type.firm, bus_type.seria FROM bus_schema.bus " \
                  "LEFT JOIN bus_schema.bus_depot AS bus_type ON bus_type.id = bus_schema.bus.bus_type_id"
        cursor.execute(sql_raw)
        result = namedtuplefetchall(cursor)

    return result


def get_params_from_config(*, ini_file: str = params.DEFAULTS_INI_FILE_PATH,
                           db_section: str = params.DEFAULTS_SECTION_NAME) -> dict:
    """
    This func return params to connect to database from ini file

    :param db_section: name of ini file with defaults
    :param ini_file: name of section with defaults in config
    """

    parser = ConfigParser()

    print_info("Reading config with default setting")
    parser.read(ini_file)

    if parser.has_section(db_section):
        db_params = parser.items(section=db_section)
        dict_params = {parameter[0]: parameter[1] for parameter in db_params}
    else:
        raise BadSectionName

    print_success("Default settings from config was successfully readed")
    return dict_params


def set_params_to_config(*, connection_parameters: dict, ini_file: str = params.CONNECTION_INI_FILE_PATH,
                         db_section: str = params.CONNECTION_SECTION_NAME) -> None:
    """
    This func return params to connect to database from ini file

    :param connection_parameters: connection params
    :param db_section: name of ini file with defaults
    :param ini_file: name of section with defaults in config
    """

    parser = ConfigParser()

    print_info("Writing connection parameters")
    parser.read(ini_file)

    if parser.has_section(db_section):
        for option, value in connection_parameters.items():
            parser.set(db_section, option, value)

        with open(ini_file, "w") as config_file:
            parser.write(config_file)
    else:
        raise BadSectionName

    print_success("Connection parameters was successfully wrote")


def connect_to_database() -> None:
    """
    This func connect to database with params from ini_file

    """

    connection = None
    try:
        params = get_params_from_config()

        print_info("Connecting to database")
        connection = psycopg2.connect(**params)
        print_success("Connection was established")

        set_params_to_config(connection_parameters=params)

    except (Exception, psycopg2.Error) as exception:
        print(exception)

    finally:
        if connection is not None and not connection.closed:
            print_info("Disconnecting from database")
            connection.close()
            print_success("Connection was closed")


if __name__ == "__main__":
    connect_to_database()
