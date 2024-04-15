import os
import yaml
from typing import Union, List
from dotenv import load_dotenv
from secure import Secure
from pathlib import Path

class Secured:
    def __init__(self, key_providers: List = None, yaml_path: str | List[str] = None) -> None:
        self.key_providers = key_providers or []
        self.yaml_files = {}
        self.yaml_data = self.load_yaml(yaml_path)

    def load_yaml(self, yaml_path: Union[str, List[str]]) -> dict:
        data = {}
        if yaml_path is None:
            return data

        yaml_paths = [yaml_path] if isinstance(yaml_path, str) else yaml_path
        for path in yaml_paths:
            with open(path, 'r') as file:
                file_data = yaml.safe_load(file)
                data.update(file_data)
                file_name = Path(path).stem
                self.yaml_files[file_name] = file_data

        return data

    def get(self, key: str, required: bool = False, dotenv_path = None) -> Union[Secure, None]:
        load_dotenv(dotenv_path)

        # Check YAML data first
        yaml_value = self.yaml_data.get(key)
        if yaml_value is not None:
            return Secure(yaml_value)

        # Check environment variables
        env_value = os.getenv(key)

        for provider in self.key_providers:
            value = provider.get(key)
            if value is not None:
                if env_value is not None:
                    raise ValueError(f"Key '{key}' exists in both OS environment and the provider.")
                return Secure(value)

        if env_value is None:
            if required:
                raise ValueError(f"Key '{key}' not found in the OS environment, the provider, or the YAML file.")

        return Secure(env_value)

    def get_yaml_file(self, path: str) -> dict:
        return self.yaml_files.get(path)
