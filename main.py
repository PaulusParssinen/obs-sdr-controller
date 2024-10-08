from __future__ import annotations

import asyncio
import logging
import time
from typing import Optional
import typing

# pyright: reportTypedDictNotRequiredAccess=false

if typing.TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3 import LiveBroadcast, LiveChatMessage

import marshmallow
import dataclasses_json
import simpleobsws

from rich.logging import RichHandler

from app_context import AppContext
from obs import OBS
from config import Config, Secrets
from youtube import YouTubeAPI
from command_handler import CommandHandler

# TODO: Configurable log level
FORMAT = "%(message)s"
logging.basicConfig(
    level=logging.DEBUG, format=FORMAT, datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, tracebacks_suppress=[
                          marshmallow, dataclasses_json, simpleobsws, asyncio])]
)

# Name of the hardcoded configuration file
CONFIG_FILE = "config/config.json"
SECRETS_FILE = "config/secrets.json"


def choose_youtube_broadcast(youtube: YouTubeAPI) -> Optional[LiveBroadcast]:
    live_broadcasts = youtube.get_live_broadcasts()
    if not live_broadcasts:
        return None

    for i, broadcast in enumerate(live_broadcasts):
        print(f"{i + 1}. {broadcast['snippet']['title']}")

    choice = int(input("Choose a broadcast: ")) - 1
    return live_broadcasts[choice]


async def listen_for_remote_commands(
        broadcast: LiveBroadcast,
        context: AppContext,
        logger: logging.Logger,
        command_handler: CommandHandler):
    live_chat_id = broadcast['snippet']['liveChatId']

    next_page_token = ''
    try:
        def handle_command(command: str, argument: str | None, _message: LiveChatMessage):
            command_handler.handle(command, argument)

        context.youtube.poll_live_chat(
            live_chat_id, next_page_token, handle_command)
    except KeyboardInterrupt:
        logger.info('Stopping the script..')
        context.event_loop.stop()

obs_ws = None
bg_tasks = set()


async def main(event_loop: asyncio.AbstractEventLoop):
    global obs_ws

    logger = logging.getLogger("obs-sdr-control")

    logger.info("Starting OBS SDR Control...")

    config: Config
    try:
        logger.info("Loading configuration...")
        config = Config.load_from_file(CONFIG_FILE)
    except:
        logger.exception("Error loading configuration. Quitting..")
        return False
    logger.info("Configuration loaded!")

    secrets: Secrets
    try:
        logger.info("Loading secrets...")
        secrets = Secrets.load_from_file(SECRETS_FILE)
    except:
        logging.info("Failed to load secrets. Creating new secrets file...")

        ws_password = input("Enter the OBS WebSocket Password: ")
        secrets = Secrets(obs_websocket_password=ws_password)

    secrets.save_to_file(SECRETS_FILE)
    logger.info("Secrets loaded!")

    logger.info("Connecting to OBS WebSocket at 'ws://%s:%s'...",
                "localhost", config.obs.websocket_port)
    obs_ws = OBS(config.obs.websocket_port, secrets.obs_websocket_password)

    logger.info("Authenticating YouTube API...")
    youtube = YouTubeAPI(config)

    broadcast = choose_youtube_broadcast(youtube)
    if not broadcast:
        logger.error("No live broadcasts found! Quitting...")
        return False

    logger.info("Loading initial state...")

    initial_preset_state = AppContext.get_preset(
        config, config.sdr.fallback.preset)

    context = AppContext(
        config,
        obs_ws,
        youtube,
        event_loop,
        current_preset_id=initial_preset_state.id,
        current_sdr_id=config.sdr.fallback.sdr,
        current_sdr_preset_state=initial_preset_state,
        config_path=CONFIG_FILE)

    cmd_handler = CommandHandler(context)

    logger.info("Starting long running tasks...")

    # TODO: Check how borked this polling logic is. Rework "threading"
    remote_loop = event_loop.create_task(
        listen_for_remote_commands(broadcast, context, logger, cmd_handler))

    # Avoid garbage collection of the task.
    bg_tasks.add(remote_loop)

    print("Listening for commands... (Ctrl+C to terminate)")
    return True

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        asyncio.run(main(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except:
        logging.exception('Critical exception:\n')
