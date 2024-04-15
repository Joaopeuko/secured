from typing import Union


class Secure(str):
    """
    A class for securing sensitive data.

    This class is designed to add a thing layer of protection by obscuring sensitive data, such as database URLs or API keys,
    in order to prevent accidental exposure in logs or debug output.

    Example:
    >>> DATABASE_URL = "your_actual_database_url"
    >>> sensitive_data = Secure(DATABASE_URL)
    >>> print(sensitive_data)
    '<Sensitive data secured>'

    """

    def __repr__(self):
        return "<Sensitive data secured>"

    def __str__(self) -> str:
        return repr(self)

    def to_int(self) -> Union[int, str]:
        try:
            return int(self)
        except ValueError:
            return self

    def to_float(self) -> Union[float, str]:
        try:
            return float(self)
        except ValueError:
            return self
