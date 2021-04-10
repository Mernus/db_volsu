DEFAULTS_INI_FILE_PATH = "configs/database_defaults.ini"  # file with default settings for connection to database
DEFAULTS_SECTION_NAME = "mongodb_defaults"  # section with default settings for needed type of database
CONNECTION_PARAMS = {"host", "database", "user", "password", "port"}

MONGO_URI = "mongodb+srv://{user}:{password}@{host}/{database}?retryWrites=true&w=majority"
