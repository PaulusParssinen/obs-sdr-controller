import logging

from app_context import AppContext


class CommandHandler:
    def __init__(self, context: AppContext):
        self.logger = logging.getLogger(__name__)
        self.context = context
        self.commands = {
            'reload': self.reload,
            'stop': self.stop,
            'scene': self.switch_scene,
        }

    def reload(self, args: str | None):
        self.logger.info("Reloading the configuration...")

        self.context.config = self.context.config.load_from_file(
            self.context.config_path)

        self.context.current_sdr_preset_state = self.context.get_preset(
            self.context.config, self.context.current_preset_id)

        self.logger.info("Configuration reloaded!")

    def stop(self, _args: str | None):
        self.logger.info("Stopping the broadcast...")
        self.context.obs.ws.stop_stream()

    def switch_scene(self, scene_name: str):
        self.logger.info("Switching scene to '%s'...", scene_name)
        self.context.obs.ws.set_current_program_scene(scene_name)

    def handle(self, command: str, argument: str | None):
        if command in self.commands:
            self.logger.debug(
                "Executing command '%s' with argument(s) '%s'...", command, argument)
            self.commands[command](argument)
        else:
            self.logger.info("Command '%s' not found!", command)
