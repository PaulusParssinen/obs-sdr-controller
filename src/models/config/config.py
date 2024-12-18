from dataclasses import dataclass
import json

from .sdr import SDRConfig
from .obs import OBSConfig
from .youtube import YoutubeConfig

from ...utils.mixins import DataClassExcludeNoneMixin

@dataclass(kw_only=True)
class Config(DataClassExcludeNoneMixin):
    version: int
    sdr: SDRConfig
    obs: OBSConfig
    youtube: YoutubeConfig

    @staticmethod
    def load_from_file(config_path: str) -> 'Config':
        with open(config_path, 'r', encoding='utf-8') as f:
            data: Config = Config.schema().load(json.load(f))
            return data

    def save_to_file(self, config_path: str):
        def clean_none(d):
            if isinstance(d, list):
                return [clean_none(v) for v in d if v is not None]
            return {k: clean_none(v) for k, v in d.items() if v is not None} if isinstance(d, dict) else d

        _config = clean_none(Config.schema().dump(self))
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(_config, f, indent=2)