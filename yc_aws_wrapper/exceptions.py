from botocore.exceptions import ClientError


def boto_exception(exception: ClientError, *args) -> bool:
    """
    :param exception:
    :param args: String variables with the name of expected errors
    :return:
    """
    if getattr(exception, "response", None) is not None:
        if "Error" in exception.response and "Code" in exception.response["Error"]:
            code = exception.response["Error"]["Code"]
            for el in args:
                if el == code:
                    return True
    return False
