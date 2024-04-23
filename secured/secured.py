import os
import yaml
from typing import Union, List, Any
from .secure import Secure
from pathlib import Path
from .attribute import AttrDict

class Secured:
    def __init__(self, yaml_paths: Union[str, List[str]] = None, secure: bool = False, as_attrdict: bool = True):
        self.as_attrdict = as_attrdict
        self.load_yaml(yaml_paths=yaml_paths, secure=secure)

    def load_yaml(self, yaml_paths: Union[str, List[str]], secure: bool):
        if not yaml_paths:
            return
        if isinstance(yaml_paths, str):
            yaml_paths = [yaml_paths]
        for path in yaml_paths:
            with open(path, 'r') as file:
                file_data = yaml.safe_load(file)
                file_name = Path(path).stem.replace('-', '_')
                setattr(self, file_name, self.create_config(file_data, secure=secure))

    def create_config(self, data: dict, secure: bool):
        if self.as_attrdict:
            return AttrDict(data, secure=secure)
        else:
            return {key: Secure(val) if secure and not isinstance(val, dict) else val 
                    for key, val in self._recursive_dict(data).items()}

    def _recursive_dict(self, data: dict):
        return {key: self._recursive_dict(val) if isinstance(val, dict) else val for key, val in data.items()}

    def get(self, key: str, required: bool = False, secure: bool = False) -> Any:
        attr_value = getattr(self, key, None)
        if attr_value is not None:
            return Secure(attr_value) if secure and not isinstance(attr_value, (AttrDict, dict)) else attr_value
        env_value = os.getenv(key)
        if env_value is not None:
            return Secure(env_value) if secure else env_value
        if required:
            raise ValueError(f"Key '{key}' not found in configuration or OS environment.")
        return None

    def use_attrdict(self, use: bool):
        self.as_attrdict = use
        for key, value in self.__dict__.items():
            if isinstance(value, (AttrDict, dict)):
                self.__dict__[key] = AttrDict(value, secure=value.secure) if use else dict(value)
