from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts.basepart import BasePart
from ..constants import SHAPEID


@dataclass
class ShortIBeam(BasePart):
    """Class that represents a Short I-Beam.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Short_I_Beam)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LongIBeam(BasePart):
    """Class that represents a Long I-Beam.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Long_I_Beam)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 4)

@dataclass
class IBeamCorner(BasePart):
    """Class that represents a I-Beam Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.I_Beam_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class IBeamHolder(BasePart):
    """Class that represents a I-Beam Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.I_Beam_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class IBeamEnd(BasePart):
    """Class that represents a I-Beam End.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.I_Beam_End)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Shelf(BasePart):
    """Class that represents a Shelf.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Shelf)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 4)

@dataclass
class StaircaseLanding(BasePart):
    """Class that represents a Staircase Landing.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Landing)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 1, 8)

@dataclass
class StaircaseLongRailing(BasePart):
    """Class that represents a Staircase Long Railing.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Long_Railing)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 6)

@dataclass
class StaircaseShortRailing(BasePart):
    """Class that represents a Staircase Short Railing.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Short_Railing)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class StaircaseBaluster(BasePart):
    """Class that represents a Staircase Baluster.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Baluster)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class StaircaseRailingJoin(BasePart):
    """Class that represents a Staircase Railing Join.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Railing_Join)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class StaircaseStep(BasePart):
    """Class that represents a Staircase Step.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Step)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 6)

@dataclass
class StaircaseBanister(BasePart):
    """Class that represents a Staircase Banister.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Banister)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 4, 1)

@dataclass
class StaircaseWedge(BasePart):
    """Class that represents a Staircase Wedge.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Wedge)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class StaircaseRamp(BasePart):
    """Class that represents a Staircase Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Staircase_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 5, 7)

@dataclass
class VentilationGrid(BasePart):
    """Class that represents a Ventilation Grid.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ventilation_Grid)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 3, 1)

@dataclass
class NetFence(BasePart):
    """Class that represents a Net Fence.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Net_Fence)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 4, 1)

@dataclass
class MetalSupport(BasePart):
    """Class that represents a Metal Support.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Support)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 4, 2)

@dataclass
class LargeSupportStructure(BasePart):
    """Class that represents a Large Support Structure.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Support_Structure)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 8, 1)

@dataclass
class SupportStructure(BasePart):
    """Class that represents a Support Structure.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Support_Structure)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 4, 1)

@dataclass
class SmallSupportStructure(BasePart):
    """Class that represents a Small Support Structure.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Support_Structure)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 1)

@dataclass
class UBeam(BasePart):
    """Class that represents a U-Beam.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.U_Beam)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 6, 1)

@dataclass
class MetalColumn(BasePart):
    """Class that represents a Metal Column.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Column)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 5, 1)

@dataclass
class SupportPillar(BasePart):
    """Class that represents a Support Pillar.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Support_Pillar)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 5)

@dataclass
class SupportPillarStand(BasePart):
    """Class that represents a Support Pillar Stand.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Support_Pillar_Stand)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 1, 7)

@dataclass
class ShelfPillar(BasePart):
    """Class that represents a Shelf Pillar.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Shelf_Pillar)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)

@dataclass
class ShelfSupport(BasePart):
    """Class that represents a Shelf Support.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Shelf_Support)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class TallShelfSupport(BasePart):
    """Class that represents a Tall Shelf Support.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tall_Shelf_Support)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 4, 1)

@dataclass
class SmallTank(BasePart):
    """Class that represents a Small Tank.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Tank)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class MediumTank(BasePart):
    """Class that represents a Medium Tank.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Medium_Tank)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 5)

@dataclass
class LargeTank(BasePart):
    """Class that represents a Large Tank.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Tank)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 5, 7)

@dataclass
class MetalWindow(BasePart):
    """Class that represents a Metal Window.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Window)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 6, 1)

@dataclass
class SteelPallet(BasePart):
    """Class that represents a Steel Pallet.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Steel_Pallet)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 1, 8)

@dataclass
class TableSupport(BasePart):
    """Class that represents a Table Support.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Table_Support)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class TowerPole(BasePart):
    """Class that represents a Tower Pole.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tower_Pole)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 8, 3)

@dataclass
class TowerPoleTop(BasePart):
    """Class that represents a Tower Pole Top.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tower_Pole_Top)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 8, 3)

@dataclass
class SatelliteDish(BasePart):
    """Class that represents a Satellite Dish.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Satellite_Dish)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 7, 1)

@dataclass
class SatelliteReflectorDish(BasePart):
    """Class that represents a Satellite Reflector Dish.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Satellite_Reflector_Dish)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 3)

@dataclass
class Antenna(BasePart):
    """Class that represents a Antenna.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Antenna)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 8, 1)

@dataclass
class ReflectorAntenna(BasePart):
    """Class that represents a Reflector Antenna.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Reflector_Antenna)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 7, 1)

@dataclass
class SmallRectangularWindow(BasePart):
    """Class that represents a Small Rectangular Window.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Rectangular_Window)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 2)

@dataclass
class SquareWindow(BasePart):
    """Class that represents a Square Window.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Square_Window)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 2)

@dataclass
class LargeRectangularWindow(BasePart):
    """Class that represents a Large Rectangular Window.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Rectangular_Window)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 4, 2)

@dataclass
class LargeWindshield(BasePart):
    """Class that represents a Large Windshield.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Windshield)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 3, 6)

@dataclass
class SmallWindshield(BasePart):
    """Class that represents a Small Windshield.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Windshield)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 5)

@dataclass
class GeneratorCoilSegment(BasePart):
    """Class that represents a Generator Coil Segment.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Coil_Segment)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 3, 6)

@dataclass
class GeneratorCoilCorner(BasePart):
    """Class that represents a Generator Coil Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Coil_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 6, 6)

@dataclass
class VentilationFrame(BasePart):
    """Class that represents a Ventilation Frame.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ventilation_Frame)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 4, 1)

@dataclass
class SteelSupportBracket(BasePart):
    """Class that represents a Steel Support Bracket.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Steel_Support_Bracket)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 4, 2)

@dataclass
class EncryptorBase(BasePart):
    """Class that represents a Encryptor Base.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Base)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 2, 3)

@dataclass
class EncryptorBasePlate(BasePart):
    """Class that represents a Encryptor Base Plate.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Base_Plate)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 1, 3)

@dataclass
class EncryptorFrameTop(BasePart):
    """Class that represents a Encryptor Frame Top.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Frame_Top)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 1, 1)

@dataclass
class SmallSteelBracket(BasePart):
    """Class that represents a Small Steel Bracket.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Steel_Bracket)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class EncryptorFrameBeam(BasePart):
    """Class that represents a Encryptor Frame Beam.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Frame_Beam)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 4, 1)

@dataclass
class EncryptorHolder(BasePart):
    """Class that represents a Encryptor Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class BaseExtension(BasePart):
    """Class that represents a Base Extension.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Base_Extension)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class GeneratorB(BasePart):
    """Class that represents a Generator B.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_B)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 8)

@dataclass
class GeneratorC(BasePart):
    """Class that represents a Generator C.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_C)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 3, 8)

@dataclass
class GeneratorD(BasePart):
    """Class that represents a Generator D.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_D)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 8)

@dataclass
class GeneratorA(BasePart):
    """Class that represents a Generator A.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_A)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 8)

@dataclass
class PowerGeneratorSide(BasePart):
    """Class that represents a Power Generator Side.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Power_Generator_Side)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 7, 1)

@dataclass
class GeneratorTank(BasePart):
    """Class that represents a Generator Tank.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Tank)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 8)

@dataclass
class GeneratorE(BasePart):
    """Class that represents a Generator E.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_E)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 8)

@dataclass
class TriggerFrame(BasePart):
    """Class that represents a Trigger Frame.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Trigger_Frame)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class GeneratorPipeHolder(BasePart):
    """Class that represents a Generator Pipe Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)