import re

from configparser import ConfigParser

from django.core.cache import cache
from django.shortcuts import redirect

from db_volsu import settings
from db_volsu.configs.params import ALL_PARAMS, DEFAULTS_INI_FILE_FULL_PATH, DEFAULTS_SECTION_NAME
from db_volsu.help_funcs.print_funcs import print_info, print_success


def update_cache_from_request(request):
    key_set = ALL_PARAMS
    cache_data = {key: request.POST[key] for key in key_set}
    if not cache_data:
        return redirect('login_page')

    cache_timeout = settings.CACHE_TTL
    cache.set_many(cache_data, timeout=cache_timeout)


def get_default_context():
    parser = ConfigParser()
    parser.read(DEFAULTS_INI_FILE_FULL_PATH)

    context = {}
    if parser.has_section(DEFAULTS_SECTION_NAME):
        db_params = parser.items(section=DEFAULTS_SECTION_NAME)
        context = {parameter[0]: parameter[1] for parameter in db_params}

    return context


def close_connection(connection):
    if connection and not connection.closed:
        print_info("Disconnecting from database")
        connection.close()
        print_success("Connection was closed")


def clear_cache():
    print_info("Clearing cache")
    cache.clear()
    print_success("Cache cleared")


def str_to_dict(str_data):
    data = {}
    for values in str_data.split(','):
        temp = re.sub('[\' ]', '', values).split('=')
        data[temp[0]] = temp[1]

    return data
