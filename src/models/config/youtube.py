from dataclasses import dataclass

from ...utils.mixins import DataClassExcludeNoneMixin

@dataclass(kw_only=True)
class YoutubeConfig(DataClassExcludeNoneMixin):
    live_chat_poll_interval: int = 10

