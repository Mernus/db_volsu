from collections import namedtuple


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def get_context(connection, sql_raw):
    with connection.cursor() as cursor:
        cursor.execute(sql_raw)
        result = namedtuplefetchall(cursor)

    return result
