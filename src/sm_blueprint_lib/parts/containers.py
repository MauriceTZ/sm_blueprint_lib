from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts.basenormalpart import BaseNormalPart
from ..constants import SHAPEID


@dataclass
class WoodenCrate(BaseNormalPart):
    """Class that represents a Wooden Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wooden_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 2)

@dataclass
class VegetableBox(BaseNormalPart):
    """Class that represents a Vegetable Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Vegetable_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 3)

@dataclass
class CucumberBox(BaseNormalPart):
    """Class that represents a Cucumber Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Cucumber_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 3)

@dataclass
class CarrotBox(BaseNormalPart):
    """Class that represents a Carrot Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Carrot_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 3)

@dataclass
class BananaBox(BaseNormalPart):
    """Class that represents a Banana Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Banana_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 3)

@dataclass
class FruitBox(BaseNormalPart):
    """Class that represents a Fruit Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fruit_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class OnionBox(BaseNormalPart):
    """Class that represents a Onion Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Onion_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 4, 4)

@dataclass
class BeetrootBox(BaseNormalPart):
    """Class that represents a Beetroot Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Beetroot_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 4, 4)

@dataclass
class OrangeBox(BaseNormalPart):
    """Class that represents a Orange Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Orange_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 6, 6)

@dataclass
class PlantContainer(BaseNormalPart):
    """Class that represents a Plant Container.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Plant_Container)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class OpenPlantContainer(BaseNormalPart):
    """Class that represents a Open Plant Container.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Open_Plant_Container)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class HayCrate(BaseNormalPart):
    """Class that represents a Hay Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Hay_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class StoneCrate(BaseNormalPart):
    """Class that represents a Stone Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Stone_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class TreeCrate(BaseNormalPart):
    """Class that represents a Tree Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tree_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class UnfoldedBananaBox(BaseNormalPart):
    """Class that represents a Unfolded Banana Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Banana_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 4)

@dataclass
class UnfoldedOnionBox(BaseNormalPart):
    """Class that represents a Unfolded Onion Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Onion_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 4)

@dataclass
class UnfoldedGrowBox(BaseNormalPart):
    """Class that represents a Unfolded Grow Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Grow_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 6)

@dataclass
class MainHumidifier(BaseNormalPart):
    """Class that represents a Main Humidifier.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Main_Humidifier)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 8)

@dataclass
class WarehouseCrate(BaseNormalPart):
    """Class that represents a Warehouse Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 8, 5)

@dataclass
class BlueberryJuiceCylinder(BaseNormalPart):
    """Class that represents a Blueberry Juice Cylinder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Blueberry_Juice_Cylinder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class TomatoJuiceCylinder(BaseNormalPart):
    """Class that represents a Tomato Juice Cylinder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tomato_Juice_Cylinder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)