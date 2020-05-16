from db_volsu.configs import params


class BadSectionName(Exception):
    """
    This exception raises if config_parser has no section with passed name

    Attributes:
        ini_file -- name of ini file with defaults
        section -- name of section with defaults in config
        message -- exception message
    """

    def __init__(self, section_name=params.DEFAULTS_SECTION_NAME, ini_filename=params.DEFAULTS_INI_FILE_PATH):
        self.section = section_name
        self.ini_file = ini_filename
        self.message = f"Can't find this section <{self.section}> in file <{self.ini_file}>"

    def __str__(self):
        formatted_message = f"[{self.__class__.__name__}]: {self.message}"
        return formatted_message
