from dataclasses import dataclass, field
from typing import Optional

from ..controllers.basecontroller import *
from .basesteering import *
from .jointwithreverse import *


@dataclass
class BaseSteeringController(BaseController):
    """Base class for Controllers that have a "steering" and the joints have a "reverse"
    attribute.
    """
    steering: Optional[list[BaseSteering]] = field(kw_only=True, default=None)
    joints: Optional[list[JointWithReverse]] = field(kw_only=True, default=None)

    def __post_init__(self):
        if self.steering:
            self.steering = [BaseSteering(**c)
                             if not isinstance(c, BaseSteering) else
                             c
                             for c in self.steering]
        if self.joints:
            self.joints = [JointWithReverse(**jj)
                           if not isinstance(jj, JointWithReverse) else
                           jj for jj in self.joints]
        super().__post_init__()

@dataclass
class BaseJointWithReverseController(BaseController):
    """Base class for Controllers where joints have a "reverse"
    attribute.
    """
    joints: Optional[list[JointWithReverse]] = field(kw_only=True, default=None)

    def __post_init__(self):
        if self.joints:
            self.joints = [JointWithReverse(**jj)
                           if not isinstance(jj, JointWithReverse) else
                           jj for jj in self.joints]
        super().__post_init__()
