import os

from db_volsu import settings

DEFAULTS_INI_FILE_PATH = "db_volsu/configs/database_defaults.ini"  # file with default settings for connection to db
DEFAULTS_INI_FILE_FULL_PATH = os.path.join(settings.BASE_DIR, DEFAULTS_INI_FILE_PATH)
DEFAULTS_SECTION_NAME = "mongodb_defaults"  # section with default settings for needed type of database

CONNECTION_PARAMS = {"host", "database", "user", "password", "port"}
ALL_PARAMS = CONNECTION_PARAMS.union({"system"})

MONGO_URI = "mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true&w=majority"

GET_OPERATIONS = ["delete"]
PERMITTED_OPERATIONS = ["update", "add"] + GET_OPERATIONS
