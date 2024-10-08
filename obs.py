import obsws_python as obsws

import logging

from config import Config


class OBS:
    def __init__(self, websocket_port: int | str, password: str, host='localhost'):
        self._ws = obsws.ReqClient(
            host=host, port=websocket_port, password=password, timeout=5)
        self.logger = logging.getLogger(__name__)

    @property
    def ws(self):
        return self._ws

    def reload(self, config: Config):
        scenes = self.ws.get_scene_list()
        self.logger.debug("Scenes: %s", scenes)
