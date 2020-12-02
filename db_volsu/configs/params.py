import re

DEFAULTS_INI_FILE_PATH = "configs/database_defaults.ini"  # file with default settings for connection to database
DEFAULTS_SECTION_NAME = "postgresql_defaults"  # section with default settings for needed type of database
CONNECTION_INI_FILE_PATH = "configs/database_connection_params.ini"  # file with connection settings for database
CONNECTION_SECTION_NAME = "connection_settings"  # section with connection settings for database
CONNECTION_PARAMS = {"host", "database", "user", "password", "port"}

_BUS_DEPOT_ROW = "SELECT * FROM bus_depot ORDER BY id;"

_USER_DATA_ROW = "SELECT * FROM user_data ORDER BY id;"

_STATION_ROW = "SELECT * FROM station ORDER BY id;"

_BUS_ROW = "SELECT bus.id AS bus_id, bus_type.firm AS bus_firm, " \
          "bus_type.seria AS bus_seria FROM bus " \
          "LEFT JOIN bus_depot AS bus_type ON bus_type.id = bus.bus_type_id ORDER BY bus_id;"

_SCHEDULE_ROW = "SELECT schedule.id AS schedule_id, " \
               "schedule.departure AS dep_station_time, dep_station.station_name AS dep_station_name, " \
               "schedule.arrival AS arr_station_time, arr_station.station_name AS arr_station_name, " \
               "bus.id, bus.firm, bus.seria " \
               "FROM schedule " \
               "LEFT JOIN station AS dep_station ON dep_station.id = schedule.point_of_departure_id " \
               "LEFT JOIN station AS arr_station ON arr_station.id = schedule.point_of_arrival_id " \
               "LEFT JOIN " \
               "( " \
               "SELECT bus.id, bus_type.firm, bus_type.seria FROM bus " \
               "LEFT JOIN bus_depot AS bus_type ON bus_type.id = bus.bus_type_id " \
               ") " \
               "AS bus ON bus.id = schedule.bus_id ORDER BY schedule_id;"

_TICKET_ROW = "SELECT ticket.id AS ticket_id, " \
             "user_d.name AS customer_name, user_d.surname AS customer_surname, user_d.mail AS customer_mail, " \
             "ticket.passenger_name, ticket.passenger_surname, " \
             "arr_station.st_time AS arr_station_time, arr_station.st_name AS arr_station_name, " \
             "dep_station.st_time AS dep_station_time, dep_station.st_name AS dep_station_name, " \
             "ticket.cost AS ticket_cost " \
             "FROM ticket " \
             "LEFT JOIN user_data AS user_d ON user_d.id = ticket.buyer_id " \
             "LEFT JOIN " \
             "( " \
             "SELECT " \
             "schedule.id AS st_id, " \
             "schedule.arrival AS st_time, " \
             "arr_station.station_name AS st_name " \
             "FROM schedule " \
             "LEFT JOIN station AS arr_station " \
             "ON arr_station.id = schedule.point_of_arrival_id " \
             ") " \
             "AS arr_station ON arr_station.st_id = ticket.route_id " \
             "LEFT JOIN " \
             "( " \
             "SELECT " \
             "schedule.id AS st_id, " \
             "schedule.departure AS st_time, " \
             "dep_station.station_name AS st_name " \
             "FROM schedule " \
             "LEFT JOIN station AS dep_station " \
             "ON dep_station.id = schedule.point_of_departure_id " \
             ") " \
             "AS dep_station ON dep_station.st_id = ticket.route_id ORDER BY ticket_id;"

_DELETE_ROW = "DELETE FROM {table} WHERE {table}.id = {row_id};"
_UPDATE_ROW = "UPDATE {table} SET {updated} WHERE {table}.id = {row_id};"

PAGE_PATTERN_COMPILED = re.compile(r"page=(\d+)", re.UNICODE)

TABLE_LIST = {
    "bus_depot": _BUS_DEPOT_ROW,
    "user_data": _USER_DATA_ROW,
    "station": _STATION_ROW,
    "bus": _BUS_ROW,
    "schedule": _SCHEDULE_ROW,
    "ticket": _TICKET_ROW
}

CHANGE_OPERATIONS = {
    "delete": _DELETE_ROW,
    "update": _UPDATE_ROW
}
