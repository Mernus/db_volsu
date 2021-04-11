class BadConnectionCredentials(Exception):
    """
    This exception raises if connection params was bad

    Attributes:
        conn_params -- connection parameters with which connection to database was failed
    """

    def __init__(self, conn_params=None):
        self.conn_params = conn_params
        self.message = f"Can't establish connection to database with this params:\n{self.conn_params}"

    def __str__(self):
        formatted_message = f"[{self.__class__.__name__}]: {self.message}"
        return formatted_message
