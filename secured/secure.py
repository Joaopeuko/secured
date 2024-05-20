from typing import Union


class Secure(str):
    def __new__(cls, original: str, message: str = "<Sensitive data secured>"):
        """
        Create a new Secure instance that appears as a custom message.

        Args:
            original: The original string to secure.
            message: A placeholder message to display instead of the original content.

        Returns:
            Secure: A new Secure instance displaying the placeholder message.
        """
        instance = super(Secure, cls).__new__(cls, original)
        instance._original = original
        instance._message = message
        return instance

    def __init__(self, original: str, message: str = "<Sensitive data secured>"):
        # Initialization handled in __new__, nothing required here
        pass

    def __repr__(self) -> str:
        """
        Represent the Secure object using the custom message.

        Returns:
            str: The custom message representing the secured data.
        """
        return self._message

    def __str__(self) -> str:
        """
        Convert the Secure object to string using the custom message.

        Returns:
            str: The custom message representing the secured data.
        """
        return self._message

    def to_int(self) -> Union[int, str]:
        """
        Try converting the original secured data to an integer.

        Returns:
            Union[int, str]: The integer value of the original data, or the custom message if conversion fails.
        """
        try:
            return int(self._original)
        except ValueError:
            return self._message

    def to_float(self) -> Union[float, str]:
        """
        Try converting the original secured data to a float.

        Returns:
            Union[float, str]: The float value of the original data, or the custom message if conversion fails.
        """
        try:
            return float(self._original)
        except ValueError:
            return self._message

    def _get_original(self) -> str:
        """
        Retrieve the original secured data.

        Returns:
            str: The original data.
        """
        return self._original
