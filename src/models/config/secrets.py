from dataclasses import dataclass
import json

from ...utils.mixins import DataClassExcludeNoneMixin

@dataclass(kw_only=True)
class Secrets(DataClassExcludeNoneMixin):
    obs_websocket_password: str

    @staticmethod
    def load_from_file(secrets_path: str):
        with open(secrets_path, 'r', encoding='utf-8') as f:
            data = Secrets.schema().load(json.load(f))
            return data

    def save_to_file(self, secrets_path: str):
        with open(secrets_path, 'w', encoding='utf-8') as f:
            json.dump(Secrets.schema().dump(self), f, indent=2)
