from typing import Any, TypeVar, Union
from .secure import Secure

T = TypeVar('T')

class AttrDict(dict):  # type: ignore
    """
    A dictionary subclass that allows attribute-style access and can optionally secure its leaf values.

    This class extends the standard dictionary to support access via attributes as well as keys. If initialized
    with `secure=True`, all non-dictionary values are wrapped using the Secure class to obscure sensitive information
    with an optional custom message.

    Attributes:
        secure (bool): Determines whether the dictionary's values should be automatically secured.
        message (str): Custom message to display when values are secured.

    Examples:
        >>> ad = AttrDict(secure=True, message="<Custom Secured>")
        >>> ad['password'] = 'my_secret'
        >>> print(ad.password)
        '<Custom Secured>'
    """

    def __init__(self, *args, secure: bool = False, message: str = "<Sensitive data secured>", **kwargs) -> None:  # type: ignore
        """
        Initialize the AttrDict with the same arguments as a normal dict, plus options to secure.

        Args:
            *args: Variable length argument list for dictionary items.
            secure: If True, non-dict values will be wrapped by the Secure class with the given message.
            message: Custom message used when values are secured.
            **kwargs: Arbitrary keyword arguments for dictionary items.
        """
        super().__init__(*args, **kwargs)
        self.secure = secure
        self.message = message
        self._convert_dicts()

    def _convert_dicts(self) -> None:
        """Recursively converts nested dictionaries into AttrDict instances and secures values if required."""
        for key, value in list(self.items()):
            self[key] = self._convert_value(value)

    def _convert_value(self, value: Union[dict, str, Any]) -> Union[Secure, 'AttrDict', Any]:
        """
        Converts and possibly secures the value based on its type and the secure setting.

        Args:
            value: The value to be converted and possibly secured.

        Returns:
            The converted value, secured if `secure` is True and not a dictionary.
        """
        if isinstance(value, dict):
            value = AttrDict(value, secure=self.secure, message=self.message)  # type: ignore
        elif self.secure and not isinstance(value, Secure):
            value = Secure(value, self.message)
        return value

    def _get_original(self, item: str) -> Any:
        """
        Retrieves the original value of the specified item, without any securing.

        Args:
            item: The attribute/key name to access.

        Returns:
            The original value associated with 'item'.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if item in self:
            value = self[item]
            if isinstance(value, Secure):
                return value._get_original()
            elif isinstance(value, AttrDict):
                return {k: v._get_original() if isinstance(v, Secure) else v for k, v in value.items()}
            else:
                return value
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __getattr__(self, item: str) -> Any:
        """
        Enables attribute-style access to dictionary keys.

        Args:
            item: The attribute/key name to access.

        Returns:
            The value associated with 'item'.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if item in self:
            return self[item] # type: ignore
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute or dictionary key to the specified value.

        Args:
            key: Attribute name or dictionary key.
            value: The value to set for the given key.

        This directly modifies the dictionary if `key` is not a special attribute.
        """
        if key in ['secure', 'message']:
            super().__setattr__(key, value)
        else:
            self[key] = self._convert_value(value)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Overrides the method to secure values when being set through item assignment.

        Args:
            key: The dictionary key where the value should be set.
            value: The value to set, which will be secured if applicable.
        """
        super().__setitem__(key, self._convert_value(value))
