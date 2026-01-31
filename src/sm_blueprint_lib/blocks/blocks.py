from dataclasses import dataclass, field

from src.sm_blueprint_lib.bases.parts.baseboundablepart import BaseBoundablePart
from src.sm_blueprint_lib.constants import SHAPEID


@dataclass
class ConcreteBlock1(BaseBoundablePart):
    """Class that represents a Concrete Block 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Concrete_Block_1)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class WoodBlock1(BaseBoundablePart):
    """Class that represents a Wood Block 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wood_Block_1)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class MetalBlock1(BaseBoundablePart):
    """Class that represents a Metal Block 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Block_1)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class BarrierBlock(BaseBoundablePart):
    """Class that represents a Barrier Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Barrier_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class TileBlock(BaseBoundablePart):
    """Class that represents a Tile Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tile_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class BrickBlock(BaseBoundablePart):
    """Class that represents a Brick Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Brick_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class GlassBlock(BaseBoundablePart):
    """Class that represents a Glass Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Glass_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class GlassTileBlock(BaseBoundablePart):
    """Class that represents a Glass Tile Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Glass_Tile_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class PathLightBlock(BaseBoundablePart):
    """Class that represents a Path Light Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Path_Light_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 2

@dataclass
class SpaceshipBlock(BaseBoundablePart):
    """Class that represents a Spaceship Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Spaceship_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class CardboardBlock(BaseBoundablePart):
    """Class that represents a Cardboard Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Cardboard_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 16

@dataclass
class ScrapWoodBlock(BaseBoundablePart):
    """Class that represents a Scrap Wood Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Scrap_Wood_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class WoodBlock2(BaseBoundablePart):
    """Class that represents a Wood Block 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wood_Block_2)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class WoodBlock3(BaseBoundablePart):
    """Class that represents a Wood Block 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wood_Block_3)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ScrapMetalBlock(BaseBoundablePart):
    """Class that represents a Scrap Metal Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Scrap_Metal_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 16

@dataclass
class MetalBlock2(BaseBoundablePart):
    """Class that represents a Metal Block 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Block_2)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class MetalBlock3(BaseBoundablePart):
    """Class that represents a Metal Block 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Block_3)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ScrapStoneBlock(BaseBoundablePart):
    """Class that represents a Scrap Stone Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Scrap_Stone_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ConcreteBlock2(BaseBoundablePart):
    """Class that represents a Concrete Block 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Concrete_Block_2)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ConcreteBlock3(BaseBoundablePart):
    """Class that represents a Concrete Block 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Concrete_Block_3)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class CrackedConcreteBlock(BaseBoundablePart):
    """Class that represents a Cracked Concrete Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Cracked_Concrete_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ConcreteSlabBlock(BaseBoundablePart):
    """Class that represents a Concrete Slab Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Concrete_Slab_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 16

@dataclass
class RustedMetalBlock(BaseBoundablePart):
    """Class that represents a Rusted Metal Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Rusted_Metal_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ExtrudedMetalBlock(BaseBoundablePart):
    """Class that represents a Extruded Metal Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Extruded_Metal_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class BubblePlasticBlock(BaseBoundablePart):
    """Class that represents a Bubble Plastic Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Bubble_Plastic_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 2

@dataclass
class PlasticBlock(BaseBoundablePart):
    """Class that represents a Plastic Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Plastic_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class InsulationBlock(BaseBoundablePart):
    """Class that represents a Insulation Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Insulation_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class PlasterBlock(BaseBoundablePart):
    """Class that represents a Plaster Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Plaster_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class CarpetBlock(BaseBoundablePart):
    """Class that represents a Carpet Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Carpet_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class PaintedWallBlock(BaseBoundablePart):
    """Class that represents a Painted Wall Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Painted_Wall_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class NetBlock(BaseBoundablePart):
    """Class that represents a Net Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Net_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 1

@dataclass
class SolidNetBlock(BaseBoundablePart):
    """Class that represents a Solid Net Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Solid_Net_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 1

@dataclass
class PunchedSteelBlock(BaseBoundablePart):
    """Class that represents a Punched Steel Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Punched_Steel_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 1

@dataclass
class StripedNetBlock(BaseBoundablePart):
    """Class that represents a Striped Net Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Striped_Net_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class SquareMeshBlock(BaseBoundablePart):
    """Class that represents a Square Mesh Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Square_Mesh_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 1

@dataclass
class RestroomBlock(BaseBoundablePart):
    """Class that represents a Restroom Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Restroom_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class DiamondPlateBlock(BaseBoundablePart):
    """Class that represents a Diamond Plate Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Diamond_Plate_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class AluminumBlock(BaseBoundablePart):
    """Class that represents a Aluminum Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Aluminum_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4

@dataclass
class WornMetalBlock(BaseBoundablePart):
    """Class that represents a Worn Metal Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Worn_Metal_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class SpaceshipFloorBlock(BaseBoundablePart):
    """Class that represents a Spaceship Floor Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Spaceship_Floor_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class SandBlock(BaseBoundablePart):
    """Class that represents a Sand Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sand_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 8

@dataclass
class ArmoredGlassBlock(BaseBoundablePart):
    """Class that represents a Armored Glass Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Armored_Glass_Block)

    def __post_init__(self):
        super().__post_init__()
        self._tiling = 4
