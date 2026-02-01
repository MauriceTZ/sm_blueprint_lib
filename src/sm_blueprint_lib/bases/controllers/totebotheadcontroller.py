from dataclasses import dataclass, field

from .basecontroller import BaseController


@dataclass
class TotebotHeadController(BaseController):
    """Totebot Head's Controller
    """
    audioIndex: int
    pitch: float
    volume: int
