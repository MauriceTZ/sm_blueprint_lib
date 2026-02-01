from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts.basenormalpart import BaseNormalPart
from ..bases.parts.baseinteractablepart import BaseInteractablePart
from ..constants import SHAPEID


@dataclass
class ToiletPaper(BaseNormalPart):
    """Class that represents a Toilet Paper.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Toilet_Paper)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sink(BaseNormalPart):
    """Class that represents a Sink.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sink)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 3, 2)

@dataclass
class Mug(BaseNormalPart):
    """Class that represents a Mug.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mug)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class MannequinBoot(BaseNormalPart):
    """Class that represents a Mannequin Boot.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mannequin_Boot)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 2)

@dataclass
class MannequinHand(BaseNormalPart):
    """Class that represents a Mannequin Hand.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mannequin_Hand)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class BabyDuckStatuette(BaseNormalPart):
    """Class that represents a Baby Duck Statuette.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Baby_Duck_Statuette)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Screw(BaseNormalPart):
    """Class that represents a Screw.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Screw)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Nut(BaseNormalPart):
    """Class that represents a Nut.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Nut)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SkullSign(BaseNormalPart):
    """Class that represents a Skull Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Skull_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class ConstructionZoneSign(BaseNormalPart):
    """Class that represents a Construction Zone Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Construction_Zone_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 1)

@dataclass
class CautionSign(BaseNormalPart):
    """Class that represents a Caution Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Caution_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 1)

@dataclass
class DangerSign(BaseNormalPart):
    """Class that represents a Danger Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Danger_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 1)

@dataclass
class StopSign(BaseNormalPart):
    """Class that represents a Stop Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Stop_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class BewareFarmbotsSign(BaseNormalPart):
    """Class that represents a Beware Farmbots Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Beware_Farmbots_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 1)

@dataclass
class WelcomeSign(BaseNormalPart):
    """Class that represents a Welcome Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Welcome_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 3, 1)

@dataclass
class DoNotEnterSign(BaseNormalPart):
    """Class that represents a Do Not Enter Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Do_Not_Enter_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class FallingObjectsSign(BaseNormalPart):
    """Class that represents a Falling Objects Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Falling_Objects_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 1)

@dataclass
class ArrowSign(BaseNormalPart):
    """Class that represents a Arrow Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Arrow_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class TrafficCone(BaseNormalPart):
    """Class that represents a Traffic Cone.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Traffic_Cone)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 3, 2)

@dataclass
class Mattress(BaseNormalPart):
    """Class that represents a Mattress.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mattress)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 2, 7)

@dataclass
class Pillow(BaseNormalPart):
    """Class that represents a Pillow.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pillow)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 2)

@dataclass
class ProduceBillboard(BaseNormalPart):
    """Class that represents a Produce Billboard.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Produce_Billboard)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 8, 1)

@dataclass
class BerryBillboard(BaseNormalPart):
    """Class that represents a Berry Billboard.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Berry_Billboard)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 8, 1)

@dataclass
class SickleDownBillboard(BaseNormalPart):
    """Class that represents a Sickle-Down Billboard.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sickle_Down_Billboard)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 8, 1)

@dataclass
class WarehouseSign(BaseNormalPart):
    """Class that represents a Warehouse Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 2, 1)

@dataclass
class ElevatorSign(BaseNormalPart):
    """Class that represents a Elevator Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Elevator_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 2, 1)

@dataclass
class StorageSign(BaseNormalPart):
    """Class that represents a Storage Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Storage_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 2, 1)

@dataclass
class PackingSign(BaseNormalPart):
    """Class that represents a Packing Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Packing_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 2, 1)

@dataclass
class OfficeSign(BaseNormalPart):
    """Class that represents a Office Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Office_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 2, 1)

@dataclass
class UtilitySign(BaseNormalPart):
    """Class that represents a Utility Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Utility_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 2, 1)

@dataclass
class ManSign(BaseNormalPart):
    """Class that represents a Man Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Man_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class WomanSign(BaseNormalPart):
    """Class that represents a Woman Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Woman_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class RecyclingBin(BaseNormalPart):
    """Class that represents a Recycling Bin.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Recycling_Bin)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 6, 3)

@dataclass
class PaperStack(BaseNormalPart):
    """Class that represents a Paper Stack.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Paper_Stack)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class OldRestroomMirror(BaseNormalPart):
    """Class that represents a Old Restroom Mirror.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Old_Restroom_Mirror)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 1)

@dataclass
class TrafficSign(BaseNormalPart):
    """Class that represents a Traffic Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Traffic_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 7, 1)

@dataclass
class MetallicTube(BaseNormalPart):
    """Class that represents a Metallic Tube.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metallic_Tube)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class RoadSignBase(BaseNormalPart):
    """Class that represents a Road Sign Base.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Road_Sign_Base)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 3)

@dataclass
class CashRegister(BaseInteractablePart):
    """Class that represents a Cash Register.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Cash_Register)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class OpenSign(BaseNormalPart):
    """Class that represents a Open Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Open_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 1)

@dataclass
class OldFruitStand(BaseNormalPart):
    """Class that represents a Old Fruit Stand.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Old_Fruit_Stand)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class StackedCrates(BaseNormalPart):
    """Class that represents a Stacked Crates.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Stacked_Crates)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 5, 4)

@dataclass
class SunshakeVendingMachine(BaseNormalPart):
    """Class that represents a Sunshake Vending Machine.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sunshake_Vending_Machine)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 8, 5)

@dataclass
class UdderDecoration(BaseNormalPart):
    """Class that represents a Udder Decoration.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Udder_Decoration)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 3, 5)

@dataclass
class Haystack(BaseNormalPart):
    """Class that represents a Haystack.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Haystack)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 4, 5)

@dataclass
class HayBale(BaseNormalPart):
    """Class that represents a Hay Bale.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Hay_Bale)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 7, 7)

@dataclass
class WindowWithBlinds(BaseNormalPart):
    """Class that represents a Window With Blinds.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Window_With_Blinds)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 6, 1)

@dataclass
class WindowWithCurtains(BaseNormalPart):
    """Class that represents a Window With Curtains.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Window_With_Curtains)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(10, 6, 1)

@dataclass
class BrokenClock(BaseNormalPart):
    """Class that represents a Broken Clock.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Broken_Clock)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)