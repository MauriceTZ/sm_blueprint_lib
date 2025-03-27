from dataclasses import dataclass, field

from ..bases.joints.suspensionjoint import SuspensionJoin
from ..constants import SHAPEID


@dataclass
class SportSuspension5(SuspensionJoin):
    """Class that represents a Sport Suspension 5 part.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Sport_Suspension_5)


@dataclass
class OffRoadSuspension5(SuspensionJoin):
    """Class that represents an Off-Road Suspension 5 part.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Off_Road_Suspension_5)
