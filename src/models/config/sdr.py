from dataclasses import dataclass, field
from typing import Any, Optional
from urllib.parse import urlencode

from ...utils.mixins import DataClassExcludeNoneMixin

@dataclass(kw_only=True)
class SDRFallbackConfig(DataClassExcludeNoneMixin):
    sdr: str
    preset: str


@dataclass(kw_only=True)
class SDRKiwiConfig(DataClassExcludeNoneMixin):
    id: str
    url: str
    name: Optional[str] = None
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
    def create_kiwi_sdr_url_query(config: 'PresetBaseConfig') -> str:
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