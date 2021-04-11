import re

from bson import ObjectId
from datetime import datetime

DATETIME_FORMAT = "%B %d, %Y, %I %p"


def parse_datetime(date):
    date = re.sub('[.]', '', date)
    return datetime.strptime(date, DATETIME_FORMAT)


TYPES_CONVERTER = {
    'str': str,
    'id': ObjectId,
    'int32': int,  # ¯\_(ツ)_/¯
    'double': float,  # ¯\_(ツ)_/¯
    'date': parse_datetime
}

TYPES = {
    'id': ["bus_type_id", "point_of_departure", "point_of_arrival", "bus_id", "customer_id"],
    'int32': ["day_route_num", "seats_num", "num_in_depot"],
    'double': ["ticket_cost", "money"],
    'date': ["dep_station_time", "arr_station_time"]
}
