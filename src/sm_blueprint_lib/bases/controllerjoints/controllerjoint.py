from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ..controllers.basecontroller import *
from .jointsetting import *

@dataclass
class ControllerJointController(BaseController):
    """Base class for Controllers that have a "joints" attribute that comes from
    the actual game's Controller part.
    """
    controllers: Optional[list[ControllerPistonControllerSetting]] = field(kw_only=True, default=None)
    joints: Optional[list[ControllerBearingJointSetting]] = field(kw_only=True, default=None)
    playMode: int
    timePerFrame: float

    def __post_init__(self):
        if self.controllers:
            self.controllers = [ControllerPistonControllerSetting(**c)
                           if not isinstance(c, ControllerPistonControllerSetting) else
                           c
                           for c in self.controllers]
        if self.joints:
            self.joints = [ControllerBearingJointSetting(**jj)
                           if not isinstance(jj, ControllerBearingJointSetting) else
                           jj
                           for jj in self.joints]
