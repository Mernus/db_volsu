from collections import namedtuple
from copy import deepcopy
from bson import ObjectId

from db_volsu.configs.psql_params import COLUMNS_ROW, IDSELECT_ROW

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def _fetch_psql(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def _fetch_mongo(docs, return_columns=False, search_filter=None):
    columns = list(docs[0].keys())
    columns.remove('_id')
    if not return_columns:
        columns.insert(0, 'id')

    result_columns = deepcopy(columns) if return_columns else None
    nt_result = namedtuple('Result', columns)

    docs_list = []
    for doc in docs:
        doc_id = doc.pop('_id')
        if not return_columns:
            doc['id'] = str(doc_id)

        add = True
        if search_filter:
            add = False

            for column, value in doc.items():
                if search_filter in str(value):
                    add = True
                    break

        if add:
            docs_list.append(nt_result(**doc))

    return docs_list, result_columns


def _fetch_all(connection, sql_raw=None, mongo=False, row_id=None, all_data=False, search_filter=None):
    columns = None

    if mongo:
        if row_id:
            object_id = ObjectId(row_id)
            docs = [connection.find_one({"_id": object_id})]
        else:
            docs = connection.find()

        result, columns = _fetch_mongo(docs, not all_data, search_filter)
        if not all_data and not row_id:
            # Bad idea, but no time to good decision
            return None, columns

    else:
        with connection.cursor() as cursor:
            cursor.execute(sql_raw)
            result = _fetch_psql(cursor)

    return result, columns


def get_context(request, connection, sql_raw=None, mongo=False, search_filter=None):
    result, _ = _fetch_all(connection, sql_raw, mongo, all_data=True, search_filter=search_filter)

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
    result, _ = _fetch_all(connection, column_row)

    return result


def get_context_by_id(connection, table_name='bus_depot', row_id=None, mongo=False):
    if not mongo:
        row = IDSELECT_ROW.format(table=table_name, row_id=row_id)

        with connection.cursor() as cursor:
            cursor.execute(row)
            result = _fetch_psql(cursor)

        return result

    result, columns = _fetch_all(connection, mongo=True, row_id=row_id)

    nt = namedtuple('Column', 'column_name')
    columns = [nt(col) for col in columns]

    return columns, result
