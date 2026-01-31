from dataclasses import dataclass, field

from glm import vec3

from ..constants import SHAPEID
from ..bases import *
from ..bases.mix import *


@dataclass
class SportSuspension1(SuspensionJoin):
    """Class that represents a Sport Suspension 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_1)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class SportSuspension2(SuspensionJoin):
    """Class that represents a Sport Suspension 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_2)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class SportSuspension3(SuspensionJoin):
    """Class that represents a Sport Suspension 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_3)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class SportSuspension4(SuspensionJoin):
    """Class that represents a Sport Suspension 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_4)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class SportSuspension5(SuspensionJoin):
    """Class that represents a Sport Suspension 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_5)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 2)

@dataclass
class OffRoadSuspension1(SuspensionJoin):
    """Class that represents a Off-Road Suspension 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_1)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class OffRoadSuspension2(SuspensionJoin):
    """Class that represents a Off-Road Suspension 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_2)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class OffRoadSuspension3(SuspensionJoin):
    """Class that represents a Off-Road Suspension 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_3)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class OffRoadSuspension4(SuspensionJoin):
    """Class that represents a Off-Road Suspension 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_4)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class OffRoadSuspension5(SuspensionJoin):
    """Class that represents a Off-Road Suspension 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_5)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 3)

@dataclass
class DriversSeat1(BaseInteractablePart):
    """Class that represents a Driver's Seat 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat_1)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class DriversSeat2(BaseInteractablePart):
    """Class that represents a Driver's Seat 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat_2)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class DriversSeat3(BaseInteractablePart):
    """Class that represents a Driver's Seat 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat_3)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class DriversSeat4(BaseInteractablePart):
    """Class that represents a Driver's Seat 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat_4)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class DriversSeat5(BaseInteractablePart):
    """Class that represents a Driver's Seat 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Seat_5)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 6)

@dataclass
class DriversSaddle1(BaseInteractablePart):
    """Class that represents a Driver's Saddle 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle_1)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class DriversSaddle2(BaseInteractablePart):
    """Class that represents a Driver's Saddle 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle_2)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class DriversSaddle3(BaseInteractablePart):
    """Class that represents a Driver's Saddle 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle_3)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class DriversSaddle4(BaseInteractablePart):
    """Class that represents a Driver's Saddle 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle_4)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class DriversSaddle5(BaseInteractablePart):
    """Class that represents a Driver's Saddle 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Drivers_Saddle_5)
    controller: ContainersSteeringController = field(default_factory=ContainersSteeringController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersSteeringController):
            self.controller = ContainersSteeringController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 5)

@dataclass
class Seat1(BaseInteractablePart):
    """Class that represents a Seat 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat_1)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class Seat2(BaseInteractablePart):
    """Class that represents a Seat 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat_2)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class Seat3(BaseInteractablePart):
    """Class that represents a Seat 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat_3)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class Seat4(BaseInteractablePart):
    """Class that represents a Seat 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat_4)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class Seat5(BaseInteractablePart):
    """Class that represents a Seat 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Seat_5)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(4, 4, 4)

@dataclass
class Saddle1(BaseInteractablePart):
    """Class that represents a Saddle 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle_1)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Saddle2(BaseInteractablePart):
    """Class that represents a Saddle 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle_2)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Saddle3(BaseInteractablePart):
    """Class that represents a Saddle 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle_3)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Saddle4(BaseInteractablePart):
    """Class that represents a Saddle 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle_4)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class Saddle5(BaseInteractablePart):
    """Class that represents a Saddle 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Saddle_5)
    controller: BaseContainersController = field(default_factory=BaseContainersController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseContainersController):
            self.controller = BaseContainersController(**self.controller)
        super().__post_init__()
        self._box = vec3(3, 4, 3)

@dataclass
class GasEngine1(BaseInteractablePart):
    """Class that represents a Gas Engine 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine_1)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class GasEngine2(BaseInteractablePart):
    """Class that represents a Gas Engine 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine_2)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class GasEngine3(BaseInteractablePart):
    """Class that represents a Gas Engine 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine_3)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class GasEngine4(BaseInteractablePart):
    """Class that represents a Gas Engine 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine_4)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class GasEngine5(BaseInteractablePart):
    """Class that represents a Gas Engine 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Gas_Engine_5)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class ElectricEngine1(BaseInteractablePart):
    """Class that represents a Electric Engine 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine_1)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class ElectricEngine2(BaseInteractablePart):
    """Class that represents a Electric Engine 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine_2)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class ElectricEngine3(BaseInteractablePart):
    """Class that represents a Electric Engine 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine_3)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class ElectricEngine4(BaseInteractablePart):
    """Class that represents a Electric Engine 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine_4)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class ElectricEngine5(BaseInteractablePart):
    """Class that represents a Electric Engine 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Electric_Engine_5)
    controller: ContainersDataJointsReverseController = field(default_factory=ContainersDataJointsReverseController)

    def __post_init__(self):
        if not isinstance(self.controller, ContainersDataJointsReverseController):
            self.controller = ContainersDataJointsReverseController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 3)

@dataclass
class Thruster1(BaseInteractablePart):
    """Class that represents a Thruster 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster_1)
    controller: BaseLevelController = field(default_factory=BaseLevelController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLevelController):
            self.controller = BaseLevelController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Thruster2(BaseInteractablePart):
    """Class that represents a Thruster 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster_2)
    controller: BaseLevelController = field(default_factory=BaseLevelController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLevelController):
            self.controller = BaseLevelController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Thruster3(BaseInteractablePart):
    """Class that represents a Thruster 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster_3)
    controller: BaseLevelController = field(default_factory=BaseLevelController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLevelController):
            self.controller = BaseLevelController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Thruster4(BaseInteractablePart):
    """Class that represents a Thruster 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster_4)
    controller: BaseLevelController = field(default_factory=BaseLevelController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLevelController):
            self.controller = BaseLevelController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Thruster5(BaseInteractablePart):
    """Class that represents a Thruster 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Thruster_5)
    controller: BaseLevelController = field(default_factory=BaseLevelController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLevelController):
            self.controller = BaseLevelController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 2, 4)

@dataclass
class Controller1(BaseInteractablePart):
    """Class that represents a Controller 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller_1)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Controller2(BaseInteractablePart):
    """Class that represents a Controller 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller_2)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Controller3(BaseInteractablePart):
    """Class that represents a Controller 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller_3)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Controller4(BaseInteractablePart):
    """Class that represents a Controller 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller_4)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Controller5(BaseInteractablePart):
    """Class that represents a Controller 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Controller_5)
    controller: ControllerJointController = field(default_factory=ControllerJointController)

    def __post_init__(self):
        if not isinstance(self.controller, ControllerJointController):
            self.controller = ControllerJointController(**self.controller)
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class Sensor1(BaseInteractablePart):
    """Class that represents a Sensor 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor_1)
    controller: SensorController = field(default_factory=SensorController)

    def __post_init__(self):
        if not isinstance(self.controller, SensorController):
            self.controller = SensorController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sensor2(BaseInteractablePart):
    """Class that represents a Sensor 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor_2)
    controller: SensorController = field(default_factory=SensorController)

    def __post_init__(self):
        if not isinstance(self.controller, SensorController):
            self.controller = SensorController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sensor3(BaseInteractablePart):
    """Class that represents a Sensor 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor_3)
    controller: SensorController = field(default_factory=SensorController)

    def __post_init__(self):
        if not isinstance(self.controller, SensorController):
            self.controller = SensorController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sensor4(BaseInteractablePart):
    """Class that represents a Sensor 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor_4)
    controller: SensorController = field(default_factory=SensorController)

    def __post_init__(self):
        if not isinstance(self.controller, SensorController):
            self.controller = SensorController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Sensor5(BaseInteractablePart):
    """Class that represents a Sensor 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sensor_5)
    controller: SensorController = field(default_factory=SensorController)

    def __post_init__(self):
        if not isinstance(self.controller, SensorController):
            self.controller = SensorController(**self.controller)
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Piston1(PistonJoint):
    """Class that represents a Piston 1.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_1)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Piston2(PistonJoint):
    """Class that represents a Piston 2.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_2)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Piston3(PistonJoint):
    """Class that represents a Piston 3.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_3)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Piston4(PistonJoint):
    """Class that represents a Piston 4.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_4)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Piston5(PistonJoint):
    """Class that represents a Piston 5.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Piston_5)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)