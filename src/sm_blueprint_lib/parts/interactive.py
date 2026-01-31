from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *

@dataclass
class Bearing(BaseJoint):
    """Class that represents a Bearing.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Bearing)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SportSuspension(SuspensionJoin):
    """Class that represents a Sport Suspension.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class OffRoadSuspension(SuspensionJoin):
    """Class that represents a Off-Road Suspension.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class DriversSeat(BaseInteractablePart):
    """Class that represents a Driver's Seat.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class Seat(BaseInteractablePart):
    """Class that represents a Seat.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class DriversSaddle(BaseInteractablePart):
    """Class that represents a Driver's Saddle.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class Saddle(BaseInteractablePart):
    """Class that represents a Saddle.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Toilet(BaseInteractablePart):
    """Class that represents a Toilet.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Toilet)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class GasEngine(BaseInteractablePart):
    """Class that represents a Gas Engine.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine)
    controller: GearController = field(default_factory=GearController)

    def __post_init__(self):
        if not isinstance(self.controller, GearController):
            self.controller = GearController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class ElectricEngine(BaseInteractablePart):
    """Class that represents a Electric Engine.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class Thruster(BaseInteractablePart):
    """Class that represents a Thruster.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Controller(BaseInteractablePart):
    """Class that represents a Controller.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Switch(BaseLogicPart):
    """Class that represents a Switch.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Switch)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Button(BaseInteractablePart):
    """Class that represents a Button.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Button)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sensor(BasePart):
    """Class that represents a Sensor.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Radio(BaseLogicPart):
    """Class that represents a Radio.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Radio)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 1)

@dataclass
class Horn(BaseInteractablePart):
    """Class that represents a Horn.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Horn)
    controller: ContainersDataController

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataController):
            self.controller = ContainersDataController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LogicGate(BaseLogicPart):
    """Class that represents a Logic Gate.
    """
    controller: LogicGateController = field(
        default_factory=LogicGateController)
    shapeId: str = field(kw_only=True, default=SHAPEID.Logic_Gate)

    def __post_init__(self):
        # Can specify mode as a dict, a tuple (mode,) or just the parameter mode
        if not isinstance(self.controller, LogicGateController):
            try:
                self.controller = LogicGateController(**self.controller)
            except TypeError:
                try:
                    self.controller = LogicGateController(*self.controller)
                except TypeError:
                    self.controller = LogicGateController(self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Timer(BasePart):
    """Class that represents a Timer.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Timer)
    controller: TimerController = field(default_factory=TimerController)

    def __post_init__(self):
        # Can provide seconds and ticks as a the TimerController class itself, a dict or a tuple (seconds, tick)
        if not isinstance(self.controller, TimerController):
            try:
                self.controller = TimerController(**self.controller)
            except TypeError:
                self.controller = TimerController(*self.controller)
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class TotebotHead_Bass(BaseTotebotHeadPart):
    """Class that represents a Totebot Head: Bass.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Totebot_Head_Bass)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class TotebotHead_Percussion(BaseTotebotHeadPart):
    """Class that represents a Totebot Head: Percussion.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Totebot_Head_Percussion)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class TotebotHead_SynthVoice(BaseTotebotHeadPart):
    """Class that represents a Totebot Head: Synth Voice.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Totebot_Head_Synth_Voice)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class TotebotHead_Blip(BaseTotebotHeadPart):
    """Class that represents a Totebot Head: Blip.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Totebot_Head_Blip)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class Bathtub(BaseInteractablePart):
    """Class that represents a Bathtub.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Bathtub)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 3, 7)

@dataclass
class Piston(PistonJoint):
    """Class that represents a Piston.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class RaftSharkMount(BaseInteractablePart):
    """Class that represents a Raft Shark Mount.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Raft_Shark_Mount)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 4, 2)

@dataclass
class MountableSpudGun(BasePart):
    """Class that represents a Mountable Spud Gun.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mountable_Spud_Gun)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 4)

@dataclass
class SmallExplosiveCanister(BaseInteractablePart):
    """Class that represents a Small Explosive Canister.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Explosive_Canister)
    controller: BaseContainersController

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class LargeExplosiveCanister(BaseInteractablePart):
    """Class that represents a Large Explosive Canister.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Explosive_Canister)
    controller: BaseContainersController

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Fridge(BasePart):
    """Class that represents a Fridge.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fridge)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 2)

@dataclass
class Locker(BasePart):
    """Class that represents a Locker.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Locker)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 7, 2)

@dataclass
class FileCabinet(BasePart):
    """Class that represents a File Cabinet.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.File_Cabinet)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class Chest(BasePart):
    """Class that represents a Chest.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Chest)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 3)

@dataclass
class Protector_AntiDestruction(BasePart):
    """Class that represents a Protector: Anti-Destruction.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Protector_Anti_Destruction)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 1)

@dataclass
class Encryptor_AntiConnection(BasePart):
    """Class that represents a Encryptor: Anti-Connection.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Encryptor_Anti_Connection)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 4, 1)

@dataclass
class OilyToiletSeat(BasePart):
    """Class that represents a Oily Toilet Seat.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Oily_Toilet_Seat)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 2, 3)

@dataclass
class Dressbot(BasePart):
    """Class that represents a Dressbot.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Dressbot)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 8, 5)

@dataclass
class MountableSpudGun(BasePart):
    """Class that represents a Mountable Spud Gun.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Mountable_Spud_Gun)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 4)

@dataclass
class RespawnBed(BasePart):
    """Class that represents a Respawn Bed.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Respawn_Bed)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 7)

# @dataclass
# class obj_interactive_builderguideblock(BasePart):
#     """Class that represents a obj_interactive_builderguideblock.
#     """
#     shapeId: str = field(kw_only=True, default=SHAPEID.obj_interactive_builderguideblock)

#     def __post_init__(self):
#         super().__post_init__()
#         self._box = vec3(4, 1, 3)