import os
from typing import Union, List
from dotenv import load_dotenv
from .secure import Secure

class Secured:
    def __init__(self, key_providers: List = None) -> None:
        self.key_providers = key_providers or []

    def get(self, key: str, required: bool = False, dotenv_path = None) -> Union[Secure, None]:
        load_dotenv(dotenv_path)
        env_value = os.getenv(key)

        for provider in self.key_providers:
            value = provider.get(key)
            if value is not None:
                if env_value is not None:
                    raise ValueError(f"Key '{key}' exists in both OS environment and the provider.")
                return Secure(value)

        if env_value is None:
            if required:
                raise ValueError(f"Key '{key}' not found in the OS environment or the provider.")

        return Secure(env_value)