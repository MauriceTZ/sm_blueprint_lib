from dataclasses import dataclass, field
from typing import Any, Optional

from .containers import *
from .data import *
from .steering import *


@dataclass
class ContainersDataController(BaseContainersController, BaseDataController):
    """Base class for Controllers that have "containers" and "data" attributes.
    """

    def __post_init__(self):
        BaseContainersController.__post_init__(self)
        BaseDataController.__post_init__(self)

@dataclass
class ContainersSteeringController(BaseContainersController, BaseSteeringController):
    """Base class for Controllers that have "containers" and "steering" attributes.
    """

    def __post_init__(self):
        BaseContainersController.__post_init__(self)
        BaseSteeringController.__post_init__(self)

@dataclass
class ContainersDataJointsReverseController(BaseContainersController, BaseDataController, BaseJointWithReverseController):
    """Base class for Controllers that have "containers", "data" and joints with "reverse" attributes.
    """

    def __post_init__(self):
        BaseContainersController.__post_init__(self)
        BaseDataController.__post_init__(self)
        BaseJointWithReverseController.__post_init__(self)
