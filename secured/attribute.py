from typing import Any, Dict, TypeVar, Union
from .secure import Secure

# A type variable that can be any type.
T = TypeVar('T')

class AttrDict(dict):
    """
    A dictionary subclass that allows attribute-style access and can optionally secure its leaf values.

    This class extends the standard dictionary to support access via attributes as well as keys. If initialized
    with `secure=True`, all non-dictionary values are wrapped using the Secure class to obscure sensitive information.

    Attributes:
        secure (bool): Determines whether the dictionary's values should be automatically secured.

    Examples:
        >>> ad = AttrDict(secure=True)
        >>> ad['password'] = 'my_secret'
        >>> print(ad.password)  # Assuming Secure.__str__() returns '<Secured>'
        '<Secured>'
    """

    def __init__(self, *args, secure: bool = False, **kwargs) -> None:
        """
        Initialize the AttrDict with the same arguments as a normal dict, plus a `secure` option.

        Args:
            *args: Variable length argument list for dictionary items.
            secure (bool): If True, non-dict values will be wrapped by the Secure class.
            **kwargs: Arbitrary keyword arguments for dictionary items.
        """
        super().__init__(*args, **kwargs)
        self.secure = secure
        self._convert_dicts()

    def _convert_dicts(self) -> None:
        """Recursively converts nested dictionaries into AttrDict instances and secures values if required."""
        for key, value in list(self.items()):
            self[key] = self._convert_value(value)

    def _convert_value(self, value: Any) -> Union[T, 'Secure']:
        """
        Converts and possibly secures the value based on its type and the secure setting.

        Args:
            value (Any): The value to be converted and possibly secured.

        Returns:
            Union[T, Secure]: The converted value, secured if `secure` is True and not a dictionary.
        """
        if isinstance(value, dict):
            return AttrDict(value, secure=self.secure)
        elif self.secure:
            return Secure(value)
        return value

    def __getattr__(self, item: str) -> Union[T, 'Secure']:
        """
        Enables attribute-style access to dictionary keys.

        Args:
            item (str): The attribute/key name to access.

        Returns:
            Union[T, Secure]: The value associated with 'item'.

        Raises:
            AttributeError: If the attribute does not exist.
        """
        if item in self:
            return self[item]
        else:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Sets the attribute or dictionary key to the specified value.

        Args:
            key (str): Attribute name or dictionary key.
            value (Any): The value to set for the given key.

        This directly modifies the dictionary if `key` is not a special attribute.
        """
        if key in ['secure', '_initializing']:
            super().__setattr__(key, value)
        else:
            self[key] = self._convert_value(value)

    def __setitem__(self, key: str, value: Any) -> None:
        """
        Overrides the method to secure values when being set through item assignment.

        Args:
            key (str): The dictionary key where the value should be set.
            value (Any): The value to set, which will be secured if applicable.
        """
        super().__setitem__(key, self._convert_value(value))
