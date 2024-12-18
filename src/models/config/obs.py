
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
