from collections import namedtuple


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
