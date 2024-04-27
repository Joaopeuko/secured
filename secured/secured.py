import os
import yaml # type: ignore
from typing import List, Dict, Any

from .log_manager import setup_default_logger
from .secure import Secure
from pathlib import Path
from .attribute import AttrDict

class Secured:
    def __init__(self, yaml_paths: str | List[str] = None, secure: bool = False, # type: ignore
                 as_attrdict: bool = True, message: str = "<Sensitive data secured>", logger=None):
        """
        Initialize a Secured object to manage YAML configuration securely.

        Args:
            yaml_paths: Paths to YAML files that should be loaded.
            secure: Flag to determine if data should be secured. Defaults to False.
            as_attrdict: If True, loaded data will be stored as AttrDict objects. Defaults to True.
            message: Custom message to use when data is secured. Defaults to "<Sensitive data secured>".
            logger: External logger for logging messages, can be None. If None, a default logger is created.
        """
        self.as_attrdict = as_attrdict
        self.secure = secure
        self.message = message
        self.logger = logger or setup_default_logger()
        self.load_yaml(yaml_paths=yaml_paths, secure=secure)


    def load_yaml(self, yaml_paths: str | List[str], secure: bool) -> None:
        """
        Load and process YAML files from specified paths.

        Args:
        yaml_paths: Paths to the YAML configuration files.
        secure: Indicates if the data should be secured.

        Processes each YAML file, converting content to AttrDict or secure data structures as required.
        """
        if not yaml_paths:
            return
        yaml_paths = [yaml_paths] if isinstance(yaml_paths, str) else yaml_paths

        for path in yaml_paths:
            try:
                with open(path, 'r') as file:
                    file_data = yaml.safe_load(file)
                file_name = Path(path).stem.replace('-', '_')
                setattr(self, file_name, self.create_config(file_data, secure=secure))
            except FileNotFoundError:
                self.logger.error(f"File {path} not found.")
                continue
            except yaml.YAMLError as e:
                self.logger.error(f"Error parsing YAML file {path}: {e}")
                continue

    def create_config(self, data:  Dict[str, Any], secure: bool) ->  Dict[str, Any]:  # type: ignore
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

    def _recursive_dict(self, data:  Dict[str, Any]) -> Dict[str, Any]:  # type: ignore[type-arg]
        """
        Recursively parse and secure dictionary data.

        Args:
            data: Data to parse.

        Returns:
            Parsed data, potentially secured.
        """
        return {key: self._recursive_dict(val) if isinstance(val, dict) else val for key, val in data.items()}

    def get(self, key: str, required: bool = False) -> Secure | None:
        """
        Retrieve configuration value by key, securing it.

        Args:
            key: The key for the configuration value.
            required: Whether the key is required (raises an error if not found).

        Returns:
            The value associated with the key, secured.
        Raises:
            ValueError: If the key is required but not found.
        """
        env_value = os.getenv(key)
        if env_value is not None:
            return Secure(env_value, self.message)
        if required:
            self.logger.error(f"Key '{key}' not found in configuration or OS environment.")
            raise ValueError(f"Key '{key}' not found.")
        return None

    def use_attrdict(self, use: bool) -> None:
        """
        Toggle the use of AttrDict for storing data.

        Args:
            use: Flag indicating whether to use AttrDict.
        """
        self.as_attrdict = use
        for key, value in self.__dict__.items():
            if isinstance(value, (AttrDict, dict)):
                self.__dict__[key] = AttrDict(value, secure=self.secure) if use else dict(value) # type: ignore
