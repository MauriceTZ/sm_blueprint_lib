from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts import *
from ..constants import SHAPEID
from ..bases.mix import *


@dataclass
class GreenTotebotCapsule(BaseInteractablePart):
    """Class that represents a Green Totebot Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Green_Totebot_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class HaybotCapsule(BaseInteractablePart):
    """Class that represents a Haybot Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Haybot_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(9, 9, 9)

@dataclass
class TapebotCapsule(BaseInteractablePart):
    """Class that represents a Tapebot Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tapebot_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(6, 9, 6)

@dataclass
class RedTapebotCapsule(BaseInteractablePart):
    """Class that represents a Red Tapebot Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Red_Tapebot_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(6, 9, 6)

@dataclass
class FarmbotCapsule(BaseInteractablePart):
    """Class that represents a Farmbot Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Farmbot_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(19, 14, 19)

@dataclass
class GlowbugCapsule(BaseInteractablePart):
    """Class that represents a Glowbug Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Glowbug_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class WocCapsule(BaseInteractablePart):
    """Class that represents a Woc Capsule.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Woc_Capsule)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(11, 9, 11)
