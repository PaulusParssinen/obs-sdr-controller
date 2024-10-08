import asyncio
from dataclasses import dataclass

from obs import OBS
from config import Config, PresetBaseConfig, PresetConfig
from youtube import YouTubeAPI


@dataclass
class AppContext:
    """A mutable context bag holding the app state to be passed around in the command handling."""
    config: Config
    obs: OBS
    youtube: YouTubeAPI
    event_loop: asyncio.AbstractEventLoop
    current_preset_id: str
    current_sdr_id: str
    config_path: str
    current_sdr_preset_state: PresetBaseConfig

    @staticmethod
    def get_sdr(config: Config, sdr_id: str):
        sdr = next(
            (s for s in config.sdr.kiwis if s.id.casefold() == sdr_id.casefold()), None)
        if not sdr:
            raise ValueError(
                f"SDR with ID '{sdr_id}' not found in the configuration!")
        return sdr

    @staticmethod
    def get_preset(config: Config, preset_id: str):
        """Builds overlays the specified preset on top of the base preset in the configuration."""
        preset = next(
            (p for p in config.sdr.presets if p.id.casefold() == preset_id.casefold()), None)
        if not preset:
            raise ValueError(f"Preset with ID '{
                             preset_id}' not found in the configuration!")

        # Overlay the preset on top of the base preset
        merged_preset = config.sdr.base_preset.__dict__.copy()
        merged_preset.update((k, v)
                             for k, v in preset.__dict__.items() if v is not None)
        return PresetConfig(**merged_preset)
