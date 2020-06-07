def print_success(unformatted_string: str) -> None:
    """
    Print for successful action info

    :param unformatted_string:
    """

    print(" [SUCCESS]: {}".format(unformatted_string))


def print_error(unformatted_string: str) -> None:
    """
    Print for error or exception action info

    :param unformatted_string:
    """

    print(" [ERROR]: {}".format(unformatted_string))


def print_info(unformatted_string: str) -> None:
    """
    Print for informational messages

    :param unformatted_string:
    """

    print(" [INFO]: {}".format(unformatted_string))
