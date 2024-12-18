import logging
from typing import Optional, TYPE_CHECKING

import click

from app_context import AppContext

# pyright: reportTypedDictNotRequiredAccess=false

if TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3 import LiveBroadcast, LiveChatMessage


class CommandHandler:
    def __init__(self, context: AppContext):
        self.logger = logging.getLogger(__name__)
        self.context = context

    @click.group()
    def cli(self):
        self.logger.info("cli called")
        pass

    # !preset [preset_id] [?freq] or !preset [preset_id] set [field] [value]
    @cli.group()
    def preset():
        """Switches to a preset or updates its field."""
        pass

    @preset.command('switch')
    @click.argument('preset_id')
    @click.argument('freq', required=False, type=float)
    def preset_switch(preset_id, freq):
        """Switch to a preset and optionally set the frequency."""
        click.echo(f"Switching to preset {preset_id}")
        if freq:
            click.echo(f"Overriding frequency to {freq}")

    @preset.command('set')
    @click.argument('preset_id')
    @click.argument('field')
    @click.argument('value')
    def preset_set(preset_id, field, value):
        """Edit the persistent preset values."""
        click.echo(f"Setting {field} of preset {preset_id} to {value}")

    # !set [field] [value]
    @cli.command()
    @click.argument('field')
    @click.argument('value')
    def set(field, value):
        """Updates the given field."""
        click.echo(f"Setting {field} to {value}")

    # !sdr [sdr_id] [?preset_id] [?freq]
    @cli.command()
    @click.argument('sdr_id')
    @click.argument('preset_id', required=False)
    @click.argument('freq', required=False, type=float)
    def sdr(sdr_id, preset_id, freq):
        """Switch to a specific SDR, and optionally a preset and frequency."""
        click.echo(f"Switching to SDR {sdr_id}")
        if preset_id:
            click.echo(f"Switching to preset {preset_id}")
        if freq:
            click.echo(f"Setting frequency to {freq}")

    # !fallback
    @cli.command()
    def fallback():
        """Resets to the fallback configuration."""
        click.echo("Resetting to fallback configuration")

    # !reload preset/config/browser
    @cli.command()
    @click.argument('target', type=click.Choice(['preset', 'config', 'browser'], case_sensitive=False))
    def reload(target):
        """Reloads the specified target (preset, config, or browser)."""
        click.echo(f"Reloading {target}")

    # Admin-only commands
    @cli.group()
    def admin():
        """Admin-only commands."""
        pass

    # !users add/remove [user]
    @admin.command()
    @click.argument('action', type=click.Choice(['add', 'remove'], case_sensitive=False))
    @click.argument('user')
    def users(action, user):
        """Manage users by adding or removing them."""
        click.echo(f"{action}ing user {user}")

    # !mute on/off
    @admin.command()
    @click.argument('state', type=click.Choice(['on', 'off'], case_sensitive=False))
    def mute(state):
        """Mute or unmute the browser OBS source."""
        click.echo(f"Muting: {state == 'on'}")

    # !stop
    @admin.command()
    def stop():
        """Terminates the OBS broadcast."""
        click.echo("Stopping OBS broadcast")

    # !scene [obs_scene_name]
    @admin.command()
    @click.argument('scene_name')
    def scene(scene_name):
        """Switch to the specified OBS scene."""
        click.echo(f"Switching to scene {scene_name}")

    def handle(self, command: list[str], _message: 'LiveChatMessage'):
        try:
            self.cli(command)
        except Exception as e:
            self.logger.error("Error handling command '%s':", command[0])
            self.logger.exception(e)
