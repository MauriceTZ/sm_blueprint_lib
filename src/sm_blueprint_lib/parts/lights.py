from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class Headlight(BaseInteractablePart):
    """Class that represents a Headlight.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Headlight)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class WarehouseSpotlight(BaseInteractablePart):
    """Class that represents a Warehouse Spotlight.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Spotlight)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class WarehouseWallLight(BaseInteractablePart):
    """Class that represents a Warehouse Wall Light.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Wall_Light)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 2)

@dataclass
class PackingLamp(BaseInteractablePart):
    """Class that represents a Packing Lamp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Packing_Lamp)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class WarehouseFluorescentLight(BaseInteractablePart):
    """Class that represents a Warehouse Fluorescent Light.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Fluorescent_Light)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(6, 1, 2)

@dataclass
class WarehouseSquareLight(BaseInteractablePart):
    """Class that represents a Warehouse Square Light.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Square_Light)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(6, 1, 6)

@dataclass
class WarehouseSpotlight(BaseInteractablePart):
    """Class that represents a Warehouse Spotlight.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Spotlight1)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class WarehouseSpotSmall(BaseInteractablePart):
    """Class that represents a Warehouse Spot Small.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Spot_Small)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)