from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class ExitSign(BasePart):
    """Class that represents a Exit Sign.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Exit_Sign)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 1)

@dataclass
class MaintenanceShipDoor(BasePart):
    """Class that represents a Maintenance Ship Door.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Maintenance_Ship_Door)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 7, 1)

@dataclass
class ShipLight(BasePart):
    """Class that represents a Ship Light.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Light)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 8)

@dataclass
class Handle(BasePart):
    """Class that represents a Handle.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Handle)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class WarehouseBrickLamp(BasePart):
    """Class that represents a Warehouse Brick Lamp.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Brick_Lamp)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Bed(BasePart):
    """Class that represents a Bed.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Bed)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 7)

@dataclass
class BrokenMicrowave(BasePart):
    """Class that represents a Broken Microwave.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Broken_Microwave)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class CraneWheel(BasePart):
    """Class that represents a Crane Wheel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Crane_Wheel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class ShipBlinds(BasePart):
    """Class that represents a Ship Blinds.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Blinds)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 6, 1)

@dataclass
class ShipCeilingVentilation(BasePart):
    """Class that represents a Ship Ceiling Ventilation.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Ceiling_Ventilation)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(6, 1, 6)

@dataclass
class ShipShelf(BasePart):
    """Class that represents a Ship Shelf.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Shelf)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class Calendar(BasePart):
    """Class that represents a Calendar.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Calendar)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)

@dataclass
class ShipFloorTile(BasePart):
    """Class that represents a Ship Floor Tile.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Floor_Tile)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 4)

@dataclass
class ShipVentilation(BasePart):
    """Class that represents a Ship Ventilation.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Ventilation)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 1)

@dataclass
class ShipCompartment(BasePart):
    """Class that represents a Ship Compartment.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Compartment)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)

@dataclass
class ShipDualfan(BasePart):
    """Class that represents a Ship Dual fan.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Dual_fan)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 3, 1)

@dataclass
class Netframe(BasePart):
    """Class that represents a Net frame.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Net_frame)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 7, 1)

@dataclass
class Netframehatch(BasePart):
    """Class that represents a Net frame hatch.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Net_frame_hatch)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 7, 1)

@dataclass
class ShipWallPanelLarge(BasePart):
    """Class that represents a Ship Wall Panel Large.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wall_Panel_Large)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 12, 1)

@dataclass
class obj_spaceship_wall08_damaged(BasePart):
    """Class that represents a obj_spaceship_wall08_damaged.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall08_damaged)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 12, 1)

@dataclass
class obj_spaceship_wall02(BasePart):
    """Class that represents a obj_spaceship_wall02.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall02)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 12, 1)

@dataclass
class obj_spaceship_wall02_damaged(BasePart):
    """Class that represents a obj_spaceship_wall02_damaged.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall02_damaged)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 12, 1)

@dataclass
class obj_spaceship_wall01(BasePart):
    """Class that represents a obj_spaceship_wall01.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall01)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 12, 1)

@dataclass
class obj_spaceship_wall03(BasePart):
    """Class that represents a obj_spaceship_wall03.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall03)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 13, 2)

@dataclass
class obj_spaceship_wall04(BasePart):
    """Class that represents a obj_spaceship_wall04.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall04)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 13, 2)

@dataclass
class obj_spaceship_wall12(BasePart):
    """Class that represents a obj_spaceship_wall12.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall12)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 14, 4)

@dataclass
class obj_spaceship_wall12_damaged(BasePart):
    """Class that represents a obj_spaceship_wall12_damaged.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall12_damaged)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 14, 4)

@dataclass
class obj_spaceship_wall06(BasePart):
    """Class that represents a obj_spaceship_wall06.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall06)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 12, 1)

@dataclass
class obj_spaceship_wall05(BasePart):
    """Class that represents a obj_spaceship_wall05.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_wall05)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 12, 1)

@dataclass
class obj_spaceship_corner01(BasePart):
    """Class that represents a obj_spaceship_corner01.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_corner01)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 12, 2)

@dataclass
class obj_spaceship_corner01_damaged(BasePart):
    """Class that represents a obj_spaceship_corner01_damaged.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_corner01_damaged)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 12, 2)

@dataclass
class obj_spaceship_corner02(BasePart):
    """Class that represents a obj_spaceship_corner02.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_corner02)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 12, 1)

@dataclass
class obj_spaceship_corner03(BasePart):
    """Class that represents a obj_spaceship_corner03.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_corner03)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 12, 1)

@dataclass
class ShipWallPanelSmall(BasePart):
    """Class that represents a Ship Wall Panel Small.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wall_Panel_Small)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class ShipWallPanelMedium(BasePart):
    """Class that represents a Ship Wall Panel Medium.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wall_Panel_Medium)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 1)

@dataclass
class ShipWallPanelLarge(BasePart):
    """Class that represents a Ship Wall Panel Large.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wall_Panel_Large)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 1)

@dataclass
class ShipWiringShort(BasePart):
    """Class that represents a Ship Wiring Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wiring_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 5)

@dataclass
class ShipWiringLong(BasePart):
    """Class that represents a Ship Wiring Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wiring_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 2, 5)

@dataclass
class ShipWiringEnd(BasePart):
    """Class that represents a Ship Wiring End.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Wiring_End)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 3, 5)

@dataclass
class ShipFloorMold(BasePart):
    """Class that represents a Ship Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class LargeShipFloorMold(BasePart):
    """Class that represents a Large Ship Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Ship_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 2)

@dataclass
class ShipOpeningFloorMold(BasePart):
    """Class that represents a Ship Opening Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Opening_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 1, 2)

@dataclass
class SmallShipCornerFloorMold(BasePart):
    """Class that represents a Small Ship Corner Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Ship_Corner_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargeShipCornerFloorMold(BasePart):
    """Class that represents a Large Ship Corner Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Ship_Corner_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 2)

@dataclass
class DiagonalShipFloorMold(BasePart):
    """Class that represents a Diagonal Ship Floor Mold.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Diagonal_Ship_Floor_Mold)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 3)

@dataclass
class ShipVentilationPanel(BasePart):
    """Class that represents a Ship Ventilation Panel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Ship_Ventilation_Panel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 6)

@dataclass
class obj_spaceship_floor_panel(BasePart):
    """Class that represents a obj_spaceship_floor_panel.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.obj_spaceship_floor_panel)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(10, 1, 36)

@dataclass
class MasterBatteryInfoBoard(BasePart):
    """Class that represents a Master Battery Info Board.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Master_Battery_Info_Board)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 10, 1)