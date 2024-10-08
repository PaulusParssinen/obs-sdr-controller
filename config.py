from dataclasses import dataclass, field
import json
from dataclasses_json import DataClassJsonMixin, Undefined, config
from typing import Any, Literal, Optional
from urllib.parse import urlencode


class DataClassExcludeNoneMixin(DataClassJsonMixin):
    dataclass_json_config = config(
        # letter_case=LetterCase.CAMEL,
        undefined=Undefined.EXCLUDE,
        exclude=lambda f: f is None
    )["dataclasses_json"]


@dataclass(kw_only=True)
class SDRFallbackConfig(DataClassExcludeNoneMixin):
    sdr: str
    preset: str


@dataclass(kw_only=True)
class SDRKiwiConfig(DataClassExcludeNoneMixin):
    id: str
    url: str
    nickname: Optional[str] = None
    preset: Optional[str] = None


@dataclass(kw_only=True)
class PresetBaseConfig(DataClassExcludeNoneMixin):
    obs_scene: Optional[str] = None
    inherit_base_preset: Optional[bool] = None
    freq: Optional[float] = None
    mode: Optional[str] = None
    zoom: Optional[int] = None
    volume: Optional[int] = None
    pb_width: Optional[str] = None
    pb_center: Optional[str] = None
    wf_colormap: Optional[int] = None
    wf_speed: Optional[str] = None
    wf_range: Optional[str] = None
    wf_auto: Optional[bool] = None
    wf_interpolation: Optional[int] = None
    wf_contrast: Optional[int] = None
    mute: Optional[bool] = None
    mem: Optional[str] = None
    keys: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    extension: Optional[str] = None

    @staticmethod
    def create_kiwi_sdr_url_path(config: 'PresetBaseConfig') -> str:
        # TODO: Refactor preset logic into own file
        def add_param(params: dict[str, Any], key: str, value: Any):
            if value:
                params[key] = value

        params: dict[str, Any] = {}

        if config.freq:
            params['f'] = config.freq

        if config.mode is not None:
            if 'f' in params:
                params['f'] = f"{params['f']},{config.mode}"
            else:
                params['f'] = f",{config.mode}"

        add_param(params, 'z', config.zoom)
        add_param(params, 'vol', config.volume)
        add_param(params, 'pbw', config.pb_width)
        add_param(params, 'pbc', config.pb_center)
        add_param(params, 'cmap', config.wf_colormap)
        add_param(params, 'wf', config.wf_speed)
        add_param(params, 'wfm', config.wf_range)
        if config.wf_auto:
            params['wfa'] = '1'
        add_param(params, 'wfi', config.wf_interpolation)
        add_param(params, 'sqrt', config.wf_contrast)
        if config.mute:
            params['mute'] = ''
        add_param(params, 'mem', config.mem)
        add_param(params, 'keys', config.keys)
        add_param(params, 'user', config.user)
        add_param(params, 'pwd', config.password)
        add_param(params, 'ext', config.extension)

        return '?' + urlencode(params, doseq=True)


@dataclass(kw_only=True)
class PresetConfig(PresetBaseConfig):
    id: str


@dataclass(kw_only=True)
class SDRConfig(DataClassExcludeNoneMixin):
    fallback: SDRFallbackConfig
    kiwis: list[SDRKiwiConfig] = field(default_factory=list)
    base_preset: Optional[PresetBaseConfig] = None
    presets: list[PresetConfig] = field(default_factory=list)


@dataclass(kw_only=True)
class OBSBrowserSourceConfig(DataClassExcludeNoneMixin):
    name: str
    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    css: Optional[str] = None
    fps: Optional[int] = None
    fps_custom: Optional[bool] = None
    reroute_audio: Optional[bool] = None
    restart_when_active: Optional[bool] = None
    shutdown: Optional[bool] = None
    webpage_control_level: Optional[int] = None


@dataclass(kw_only=True)
class OBSSceneConfig(DataClassExcludeNoneMixin):
    name: str
    browser_source: OBSBrowserSourceConfig


@dataclass(kw_only=True)
class OBSConfig(DataClassExcludeNoneMixin):
    websocket_port: int = 4455
    websocket_password: Optional[str] = None
    scenes: list[OBSSceneConfig] = field(default_factory=list)


@dataclass(kw_only=True)
class YoutubeConfig(DataClassExcludeNoneMixin):
    live_chat_poll_interval: int = 10


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
