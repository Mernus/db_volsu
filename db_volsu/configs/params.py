DEFAULTS_INI_FILE_PATH = "configs/database_defaults.ini"  # file with default settings for connection to database
DEFAULTS_SECTION_NAME = "postgresql_defaults"  # section with default settings for needed type of database
CONNECTION_INI_FILE_PATH = "configs/database_connection_params.ini"  # file with connection settings for database
CONNECTION_SECTION_NAME = "connection_settings"  # section with connection settings for database
CONNECTION_PARAMS = {"host", "database", "user", "password", "port"}

BUS_DEPOT_RAW = "SELECT * FROM bus_schema.bus_depot"

USER_DATA_RAW = "SELECT * FROM bus_schema.user_data"

STATION_RAW = "SELECT * FROM bus_schema.station"

BUS_RAW = "SELECT bus_schema.bus.id AS bus_id, bus_type.firm AS bus_firm, " \
          "bus_type.seria AS bus_seria FROM bus_schema.bus " \
          "LEFT JOIN bus_schema.bus_depot AS bus_type ON bus_type.id = bus_schema.bus.bus_type_id"

SCHEDULE_RAW = "SELECT bus_schema.schedule.id AS shedule_id, " \
               "bus_schema.schedule.departure AS dep_station_time, dep_station.station_name AS dep_station_name, " \
               "bus_schema.schedule.arrival AS arr_station_time, arr_station.station_name AS arr_station_name, " \
               "bus.id, bus.firm, bus.seria " \
               "FROM bus_schema.schedule " \
               "LEFT JOIN bus_schema.station AS dep_station ON dep_station.id = bus_schema.schedule.point_of_departure_id " \
               "LEFT JOIN bus_schema.station AS arr_station ON arr_station.id = bus_schema.schedule.point_of_arrival_id " \
               "LEFT JOIN " \
               "( " \
               "SELECT bus_schema.bus.id, bus_type.firm, bus_type.seria FROM bus_schema.bus " \
               "LEFT JOIN bus_schema.bus_depot AS bus_type ON bus_type.id = bus_schema.bus.bus_type_id " \
               ") " \
               "AS bus ON bus.id = bus_schema.schedule.bus_id"

TICKET_RAW = "SELECT bus_schema.ticket.id AS ticket_id, " \
             "user_d.name AS customer_name, user_d.surname AS customer_surname, user_d.mail AS customer_mail, " \
             "bus_schema.ticket.passenger_name, bus_schema.ticket.passenger_surname, " \
             "arr_station.st_time AS arr_station_time, arr_station.st_name AS arr_station_name, " \
             "dep_station.st_time AS dep_station_time, dep_station.st_name AS dep_station_name, " \
             "bus_schema.ticket.cost AS ticket_cost " \
             "FROM bus_schema.ticket " \
             "LEFT JOIN bus_schema.user_data AS user_d ON user_d.id = bus_schema.ticket.buyer_id " \
             "LEFT JOIN " \
             "( " \
             "SELECT " \
             "bus_schema.schedule.id AS st_id, " \
             "bus_schema.schedule.arrival AS st_time, " \
             "arr_station.station_name AS st_name " \
             "FROM bus_schema.schedule " \
             "LEFT JOIN bus_schema.station AS arr_station " \
             "ON arr_station.id = bus_schema.schedule.point_of_arrival_id " \
             ") " \
             "AS arr_station ON arr_station.st_id = bus_schema.ticket.route_id " \
             "LEFT JOIN " \
             "( " \
             "SELECT " \
             "bus_schema.schedule.id AS st_id, " \
             "bus_schema.schedule.departure AS st_time, " \
             "dep_station.station_name AS st_name " \
             "FROM bus_schema.schedule " \
             "LEFT JOIN bus_schema.station AS dep_station " \
             "ON dep_station.id = bus_schema.schedule.point_of_departure_id " \
             ") " \
             "AS dep_station ON dep_station.st_id = bus_schema.ticket.route_id"

DELETE_ROW = "DELETE FROM bus_schema.{table} WHERE bus_schema.{table}.id = {del_id}"
