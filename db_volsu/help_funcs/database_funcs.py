from collections import namedtuple
from copy import deepcopy
from bson import ObjectId

from db_volsu.configs.psql_params import COLUMNS_ROW, IDSELECT_ROW


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def _fetch_all(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def _fetch_mongo(docs, return_columns=False):
    columns = list(docs[0].keys())
    columns.remove('_id')
    columns.append('id')

    result_columns = deepcopy(columns) if return_columns else None
    nt_result = namedtuple('Result', columns)

    docs_list = []
    for doc in docs:
        doc['id'] = str(doc.pop('_id'))
        docs_list.append(nt_result(**doc))

    return docs_list, result_columns


def get_context(request, connection, sql_raw=None, mongo=False):
    if mongo:
        docs = connection.find()
        result, _ = _fetch_mongo(docs)

    else:
        with connection.cursor() as cursor:
            cursor.execute(sql_raw)
            result = _fetch_all(cursor)

    paginator = Paginator(result, 5)
    page_number = request.GET.get('page')

    try:
        page_result = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_result = paginator.get_page(1)
    except EmptyPage:
        page_result = paginator.get_page(paginator.num_pages)

    return page_result


def get_columns(connection, table_name='bus_depot'):
    column_row = COLUMNS_ROW.format(table=table_name)

    with connection.cursor() as cursor:
        cursor.execute(column_row)
        result = _fetch_all(cursor)

    return result


def get_context_by_id(connection, table_name='bus_depot', row_id=None, mongo=False):
    if mongo:
        object_id = ObjectId(row_id)
        row = connection.find_one({"_id": object_id})

        result, columns = _fetch_mongo([row], return_columns=True)
        columns.remove('id')

        nt = namedtuple('Column', 'column_name')
        columns = [nt(col) for col in columns]

        return columns, result

    row = IDSELECT_ROW.format(table=table_name, row_id=row_id)

    with connection.cursor() as cursor:
        cursor.execute(row)
        result = _fetch_all(cursor)

    return result
