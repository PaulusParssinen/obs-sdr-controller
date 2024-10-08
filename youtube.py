from __future__ import annotations
import logging
import time
from typing import Callable, Optional
import typing
import os
import google.auth
import google.auth.transport.requests
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from config import Config

# pyright: reportTypedDictNotRequiredAccess=false

if typing.TYPE_CHECKING:
    from googleapiclient._apis.youtube.v3 import YouTubeResource, LiveBroadcast, LiveChatMessage

TOKEN_FILE = 'config/token_secret.json'
CLIENT_SECRET_FILE = 'config/client_secret.json'

# YouTube API Scopes
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']


class YouTubeAPI:
    def __init__(self, config: Config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.youtube: YouTubeResource = self.authenticate_youtube(config)

    def authenticate_youtube(self, config: Config) -> YouTubeResource:
        credentials = None

        # Check if token file exists and load it
        if os.path.exists(TOKEN_FILE):
            credentials = Credentials.from_authorized_user_file(
                TOKEN_FILE, SCOPES)

        # If credentials are invalid or not found, prompt for re-authentication
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(google.auth.transport.requests.Request())
            else:
                self.logger.info(
                    'Re-authenticating because the refresh_token has expired...')
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES)
                credentials = flow.run_local_server(
                    port=8888, timeout_seconds=60)

            # Save the credentials for re-use
            with open(TOKEN_FILE, 'w', encoding='utf-8') as token:
                token.write(credentials.to_json())

        _youtube = build(
            'youtube', 'v3', credentials=credentials, cache_discovery=False)
        return _youtube

    def get_live_broadcasts(self) -> list[LiveBroadcast]:
        request = self.youtube.liveBroadcasts().list(
            part='snippet',
            broadcastStatus='active'
        )
        try:
            response = request.execute()
            return response['items']
        except:
            self.logger.exception('Error getting live broadcasts:\n')
            return []

    def get_live_chat_messages(self,
                               live_chat_id: str,
                               page_token: str) -> tuple[list[LiveChatMessage], str, int]:
        request = self.youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part='snippet,authorDetails',
            pageToken=page_token,
            maxResults=2000
        )
        response = request.execute()
        try:
            return response['items'], response['nextPageToken'], response['pollingIntervalMillis']
        except:
            self.logger.exception('Error getting live chat messages:\n')
            return [], '', 0

    def poll_live_chat(self,
                       live_chat_id: str,
                       page_token: str,
                       handle_command: Callable[[str, Optional[str], LiveChatMessage], None]):
        processed_messages = set()
        while True:
            messages, page_token, _ = self.get_live_chat_messages(
                live_chat_id, page_token)

            for message in messages:
                message_text = message['snippet']['textMessageDetails']['messageText']
                message_id = message['id']

                if message_id in processed_messages:
                    continue

                processed_messages.add(message_id)

                if message_text.startswith('!'):
                    cmd_parts = message_text.split(' ', 1)
                    cmd = cmd_parts[0][1:].strip()
                    arguments = cmd_parts[1].strip() if len(
                        cmd_parts) > 1 else None

                    handle_command(cmd, arguments, message)

            time.sleep(self.config.youtube.live_chat_poll_interval)
