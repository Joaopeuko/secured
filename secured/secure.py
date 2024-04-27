
class Secure(str):
    """
    A class for securing sensitive data.

    This class is designed to add a thin layer of protection by obscuring sensitive data, such as database URLs or API keys,
    in order to prevent accidental exposure in logs or debug output. The representation of the secured data can be customized
    with a specific message.

    Attributes:
        message: Custom message to represent the secured data when printed or logged.

    Example:
    >>> DATABASE_URL = "your_actual_database_url"
    >>> sensitive_data = Secure(DATABASE_URL, "<Data Hidden>")
    >>> print(sensitive_data)
    '<Data Hidden>'
    """

    def __new__(cls, original: str, message: str = "<Sensitive data secured>"):
        """
        Create a new Secure instance that appears as a custom message.

        Args:
            original: The original string to secure.
            message: A placeholder message to display instead of the original content.

        Returns:
            Secure: A new Secure instance displaying the placeholder message.
        """
        # Initialize the Secure instance with the message instead of the original content.
        return super(Secure, cls).__new__(cls, message)

    def __init__(self, original: str, message: str = "<Sensitive data secured>"):
        """
        Initializes a Secure object. The initialization logic is handled by __new__; __init__ does not
        need to handle the data directly.

        Args:
            original: The original data to secure.
            message: A custom message to use for representing the secured data.
        """
        super().__init__()
        self.original = original
        self.message = message

    def __repr__(self) -> str:
        """
        Represent the Secure object using the custom message.

        Returns:
            str: The custom message representing the secured data.
        """
        return self.message

    def __str__(self) -> str:
        """
        Convert the Secure object to string using the custom message.

        Returns:
            str: The custom message representing the secured data.
        """
        return self.__repr__()

    def to_int(self) -> int | str:
        """
        Try converting the original secured data to an integer.

        Returns:
            Union[int, str]: The integer value of the original data, or the custom message if conversion fails.
        """
        try:
            return int(self.original)
        except ValueError:
            return self.message

    def to_float(self) -> float | str:
        """
        Try converting the original secured data to a float.

        Returns:
            Union[float, str]: The float value of the original data, or the custom message if conversion fails.
        """
        try:
            return float(self.original)
        except ValueError:
            return self.message
