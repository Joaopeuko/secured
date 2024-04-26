import os
import yaml
from typing import Union, List, Any
from .secure import Secure
from pathlib import Path
from .attribute import AttrDict

class Secured:
    def __init__(self, yaml_paths: Union[str, List[str]] = None, secure: bool = False, 
                 as_attrdict: bool = True, message: str = "<Sensitive data secured>"):
        """
        Initialize a Secured object to manage YAML configuration securely.

        Args:
        yaml_paths (Union[str, List[str]], optional): Paths to YAML files that should be loaded.
        secure (bool, optional): Flag to determine if data should be secured. Defaults to False.
        as_attrdict (bool, optional): If True, loaded data will be stored as AttrDict objects. Defaults to True.
        message (str, optional): Custom message to use when data is secured. Defaults to "<Sensitive data secured>".

        Loads YAML files, creates configuration as specified by flags, and handles data securely if requested.
        """
        self.as_attrdict = as_attrdict
        self.secure = secure
        self.message = message  # Custom message for secured data
        self.load_yaml(yaml_paths=yaml_paths, secure=secure)

    def load_yaml(self, yaml_paths: Union[str, List[str]], secure: bool) -> None:
        """
        Load and process YAML files from specified paths.

        Args:
        yaml_paths (Union[str, List[str]]): Paths to the YAML configuration files.
        secure (bool): Indicates if the data should be secured.

        Processes each YAML file, converting content to AttrDict or secure data structures as required.
        """
        if not yaml_paths:
                return
        if isinstance(yaml_paths, str):
            yaml_paths = [yaml_paths]

        for path in yaml_paths:
            try:
                with open(path, 'r') as file:
                    file_data = yaml.safe_load(file)
            except FileNotFoundError:
                print(f"Error: File {path} not found.")
                continue
            except yaml.YAMLError as e:
                print(f"Error parsing YAML file {path}: {e}")
                continue

            file_name = Path(path).stem.replace('-', '_')
            setattr(self, file_name, self.create_config(file_data, secure=secure))

    def create_config(self, data: dict, secure: bool) -> Union[AttrDict, dict]:
        """
        Create a configuration from data loaded from a YAML file.

        Args:
        data (dict): Data loaded from YAML.
        secure (bool): Indicates if the data should be secured.

        Returns:
        Union[AttrDict, dict]: Configured data in the form of an AttrDict or a dictionary with secure elements.
        """
        if self.as_attrdict:
            return AttrDict(data, secure=secure, message=self.message)
        else:
            return {key: Secure(val, self.message) if secure and not isinstance(val, dict) else val
                    for key, val in self._recursive_dict(data).items()}

    def _recursive_dict(self, data: dict) -> dict:
        """
        Recursively parse and secure dictionary data.

        Args:
        data (dict): Data to parse.

        Returns:
        dict: Parsed data, potentially secured.
        """
        return {key: self._recursive_dict(val) if isinstance(val, dict) else val for key, val in data.items()}

    def get(self, key: str, required: bool = False, secure: bool = False) -> Secure | None:
        """
        Retrieve configuration value by key, optionally securing it.

        Args:
        key (str): The key for the configuration value.
        required (bool, optional): Whether the key is required (raises an error if not found).
        secure (bool, optional): Whether to secure the returned value.

        Returns:
        Any: The value associated with the key, optionally secured.

        Raises:
        ValueError: If the key is required but not found.
        """
        attr_value = getattr(self, key, None)
        if attr_value is not None:
            return Secure(attr_value, self.message) if secure and not isinstance(attr_value, (AttrDict, dict)) else attr_value
        env_value = os.getenv(key)
        if env_value is not None:
            return Secure(env_value, self.message) if secure else env_value
        if required:
            raise ValueError(f"Key '{key}' not found in configuration or OS environment.")
        return None

    def use_attrdict(self, use: bool) -> None:
        """
        Toggle the use of AttrDict for storing data.

        Args:
        use (bool): Flag indicating whether to use AttrDict.
        """
        self.as_attrdict = use
        for key, value in self.__dict__.items():
            if isinstance(value, (AttrDict, dict)):
                self.__dict__[key] = AttrDict(value, secure=value.secure) if use else dict(value)
