import os
import yaml
from typing import List
from secure import Secure
from pathlib import Path

class AttrDict(dict):
    def __init__(self, *args, secure, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.secure = secure
        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = AttrDict(value, secure=secure)

    def __getattr__(self, item):
        value = self[item]
        if isinstance(value, dict):
            return value
        else:
            return Secure(value) if self.secure else value

    def __setattr__(self, key, value):
        super(AttrDict, self).__setattr__(key, value)

class Secured:
    def __init__(self, yaml_path: str | List[str] = None, secure=False) -> None:

        self.yaml_files = self.load_yaml(yaml_path=yaml_path, secure=secure)

    def load_yaml(self, yaml_path: str | List[str], secure) -> None:
        if yaml_path is None:
            return

        yaml_paths = [yaml_path] if isinstance(yaml_path, str) else yaml_path
        for path in yaml_paths:
            with open(path, 'r') as file:
                file_data = yaml.safe_load(file)
                file_name = Path(path).stem.replace('-', '_')
                setattr(self, file_name, AttrDict(file_data, secure=secure))

    def get(self, key: str, required: bool = False) -> Secure | None:

        # Check environment variables
        env_value = os.getenv(key)

        if env_value is None:
            if required:
                raise ValueError(f"Key '{key}' not found in the OS environment.")

        return Secure(env_value)


secured = Secured('config-secrets.yaml', secure=True)

print(secured.config_secrets.test.test1.test2.test4)