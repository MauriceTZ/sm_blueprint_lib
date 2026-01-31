from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class IndustrialBeamShort(BasePart):
    """Class that represents a Industrial Beam Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)

@dataclass
class IndustrialBeamLong(BasePart):
    """Class that represents a Industrial Beam Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 6)

@dataclass
class IndustrialBeamCorner(BasePart):
    """Class that represents a Industrial Beam Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class IndustrialBeamCornerBend(BasePart):
    """Class that represents a Industrial Beam Corner Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Corner_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class IndustrialBeamFourWay(BasePart):
    """Class that represents a Industrial Beam Four Way.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Four_Way)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class IndustrialBeamCrossing(BasePart):
    """Class that represents a Industrial Beam Crossing.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_Crossing)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class IndustrialBeamEnd(BasePart):
    """Class that represents a Industrial Beam End.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Industrial_Beam_End)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)

@dataclass
class FrameBeamShort(BasePart):
    """Class that represents a Frame Beam Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Frame_Beam_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class FrameBeamLong(BasePart):
    """Class that represents a Frame Beam Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Frame_Beam_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 4)

@dataclass
class FrameBeamEnd(BasePart):
    """Class that represents a Frame Beam End.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Frame_Beam_End)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class FrameBeamCorner(BasePart):
    """Class that represents a Frame Beam Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Frame_Beam_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 2)

@dataclass
class LargeWarehouseRamp(BasePart):
    """Class that represents a Large Warehouse Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Warehouse_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallWarehouseRamp(BasePart):
    """Class that represents a Small Warehouse Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Warehouse_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargeNarrowWarehouseRamp(BasePart):
    """Class that represents a Large Narrow Warehouse Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Narrow_Warehouse_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallNarrowWarehouseRamp(BasePart):
    """Class that represents a Small Narrow Warehouse Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Narrow_Warehouse_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class MetalStorageSupport(BasePart):
    """Class that represents a Metal Storage Support.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Support)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 7)

@dataclass
class MetalStorageCornerA(BasePart):
    """Class that represents a Metal Storage Corner A.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Corner_A)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 3)

@dataclass
class MetalStorageRamp(BasePart):
    """Class that represents a Metal Storage Ramp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Ramp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargeMetalStorageLamp(BasePart):
    """Class that represents a Large Metal Storage Lamp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Metal_Storage_Lamp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class MetalStorageBeam(BasePart):
    """Class that represents a Metal Storage Beam.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Beam)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 8)

@dataclass
class MetalStorageCornerB(BasePart):
    """Class that represents a Metal Storage Corner B.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Corner_B)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 3, 2)

@dataclass
class MetalStorageCornerC(BasePart):
    """Class that represents a Metal Storage Corner C.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Corner_C)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class MetalStorageHandle(BasePart):
    """Class that represents a Metal Storage Handle.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Handle)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class MetalStorageFloor(BasePart):
    """Class that represents a Metal Storage Floor.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Metal_Storage_Floor)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 1, 8)

@dataclass
class FanBase(BasePart):
    """Class that represents a Fan Base.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fan_Base)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 7, 1)

@dataclass
class FanBladeCap(BasePart):
    """Class that represents a Fan Blade Cap.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fan_Blade_Cap)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class FanBlade(BasePart):
    """Class that represents a Fan Blade.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fan_Blade)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)

@dataclass
class PackingTable(BasePart):
    """Class that represents a Packing Table.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Packing_Table)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 1, 6)

@dataclass
class PackingTableHolder(BasePart):
    """Class that represents a Packing Table Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Packing_Table_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 5, 1)

@dataclass
class PackInstructionSign(BasePart):
    """Class that represents a Pack Instruction Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pack_Instruction_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 2, 1)

@dataclass
class WrappingRoll(BasePart):
    """Class that represents a Wrapping Roll.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wrapping_Roll)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 4)

@dataclass
class Banner(BasePart):
    """Class that represents a Banner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Banner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 7, 1)

@dataclass
class BannerHolder(BasePart):
    """Class that represents a Banner Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Banner_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 1, 4)

@dataclass
class FrameBeamLight(BaseInteractablePart):
    """Class that represents a Frame Beam Light.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Frame_Beam_Light)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class CraneLeg(BasePart):
    """Class that represents a Crane Leg.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Leg)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 5, 2)

@dataclass
class CranePanel(BasePart):
    """Class that represents a Crane Panel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Panel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 4, 1)

@dataclass
class CraneCableRoll(BasePart):
    """Class that represents a Crane Cable Roll.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Cable_Roll)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 7, 5)

@dataclass
class CraneTop(BasePart):
    """Class that represents a Crane Top.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Top)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 6)

@dataclass
class CraneBody(BasePart):
    """Class that represents a Crane Body.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Body)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 4)

@dataclass
class CraneHook(BasePart):
    """Class that represents a Crane Hook.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Hook)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 1)

@dataclass
class CraneHookBlock(BasePart):
    """Class that represents a Crane Hook Block.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Hook_Block)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 5, 3)

@dataclass
class CraneLoadingFloor(BasePart):
    """Class that represents a Crane Loading Floor.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Loading_Floor)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 1, 7)

@dataclass
class ProtectorSign(BaseInteractablePart):
    """Class that represents a Protector Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Protector_Sign)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(8, 4, 2)

@dataclass
class EncryptorSign(BaseInteractablePart):
    """Class that represents a Encryptor Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Sign)
    controller: LightController = field(kw_only=True, default_factory=LightController)

    def __post_init__(self):
        if not isinstance(self.controller, LightController):
            self.controller = LightController(**self.controller)
        super().__post_init__()
        self._box = vec3(8, 4, 2)

@dataclass
class MasterSwitch(BaseLogicPart):
    """Class that represents a Master Switch.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Master_Switch)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 1)