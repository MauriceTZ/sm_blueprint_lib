from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts.basepart import BasePart
from ..constants import SHAPEID


@dataclass
class WoodenCrate(BasePart):
    """Class that represents a Wooden Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wooden_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 2)

@dataclass
class VegetableBox(BasePart):
    """Class that represents a Vegetable Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Vegetable_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 3)

@dataclass
class CucumberBox(BasePart):
    """Class that represents a Cucumber Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Cucumber_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 3)

@dataclass
class CarrotBox(BasePart):
    """Class that represents a Carrot Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Carrot_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 3)

@dataclass
class BananaBox(BasePart):
    """Class that represents a Banana Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Banana_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 3)

@dataclass
class FruitBox(BasePart):
    """Class that represents a Fruit Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fruit_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class OnionBox(BasePart):
    """Class that represents a Onion Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Onion_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 4, 4)

@dataclass
class BeetrootBox(BasePart):
    """Class that represents a Beetroot Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Beetroot_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 4, 4)

@dataclass
class OrangeBox(BasePart):
    """Class that represents a Orange Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Orange_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 6, 6)

@dataclass
class PlantContainer(BasePart):
    """Class that represents a Plant Container.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Plant_Container)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class OpenPlantContainer(BasePart):
    """Class that represents a Open Plant Container.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Open_Plant_Container)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class HayCrate(BasePart):
    """Class that represents a Hay Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Hay_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class StoneCrate(BasePart):
    """Class that represents a Stone Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Stone_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class TreeCrate(BasePart):
    """Class that represents a Tree Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tree_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 7)

@dataclass
class UnfoldedBananaBox(BasePart):
    """Class that represents a Unfolded Banana Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Banana_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 4)

@dataclass
class UnfoldedOnionBox(BasePart):
    """Class that represents a Unfolded Onion Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Onion_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 4)

@dataclass
class UnfoldedGrowBox(BasePart):
    """Class that represents a Unfolded Grow Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Unfolded_Grow_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 6)

@dataclass
class MainHumidifier(BasePart):
    """Class that represents a Main Humidifier.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Main_Humidifier)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 8)

@dataclass
class WarehouseCrate(BasePart):
    """Class that represents a Warehouse Crate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Crate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 8, 5)

@dataclass
class BlueberryJuiceCylinder(BasePart):
    """Class that represents a Blueberry Juice Cylinder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Blueberry_Juice_Cylinder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class TomatoJuiceCylinder(BasePart):
    """Class that represents a Tomato Juice Cylinder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tomato_Juice_Cylinder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)