def print_success(unformatted_string: str) -> None:
    """
    Print for successful action info

    :param unformatted_string:
    """

    print("\033[32m [SUCCESS]: {} \033[0m".format(unformatted_string))


def print_error(unformatted_string: str) -> None:
    """
    Print for error or exception action info

    :param unformatted_string:
    """

    print("\033[31m [ERROR]: {} \033[0m".format(unformatted_string))


def print_info(unformatted_string: str) -> None:
    """
    Print for informational messages

    :param unformatted_string:
    """

    print(" [INFO]: {}".format(unformatted_string))
