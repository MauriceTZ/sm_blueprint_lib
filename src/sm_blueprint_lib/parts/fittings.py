from dataclasses import dataclass, field

from glm import vec3

from ..bases.parts.basepart import BasePart
from ..constants import SHAPEID


@dataclass
class DuctShort(BasePart):
    """Class that represents a Duct Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class DuctLong(BasePart):
    """Class that represents a Duct Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 2, 1)

@dataclass
class DuctCorner(BasePart):
    """Class that represents a Duct Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class DuctJoin(BasePart):
    """Class that represents a Duct Join.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_Join)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class DuctHolder(BasePart):
    """Class that represents a Duct Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class DuctEnd(BasePart):
    """Class that represents a Duct End.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Duct_End)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class AirConditioner(BasePart):
    """Class that represents a Air Conditioner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Air_Conditioner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 3, 2)

@dataclass
class PipeShort(BasePart):
    """Class that represents a Pipe Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pipe_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class PipeLong(BasePart):
    """Class that represents a Pipe Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pipe_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)

@dataclass
class PipeCorner(BasePart):
    """Class that represents a Pipe Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pipe_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class PipeJoin(BasePart):
    """Class that represents a Pipe Join.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Pipe_Join)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class Valve(BasePart):
    """Class that represents a Valve.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Valve)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargePipeShort(BasePart):
    """Class that represents a Large Pipe Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class LargePipeLong(BasePart):
    """Class that represents a Large Pipe Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 6, 3)

@dataclass
class LargePipeCorner(BasePart):
    """Class that represents a Large Pipe Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class LargePipeJoin(BasePart):
    """Class that represents a Large Pipe Join.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Join)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class WiresShort(BasePart):
    """Class that represents a Wires Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wires_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class WiresLong(BasePart):
    """Class that represents a Wires Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wires_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 5, 1)

@dataclass
class WiresBend(BasePart):
    """Class that represents a Wires Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wires_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class WiresConvexBend(BasePart):
    """Class that represents a Wires Convex Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wires_Convex_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class WiresConcaveBend(BasePart):
    """Class that represents a Wires Concave Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Wires_Concave_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 1, 1)

@dataclass
class FuseBox(BasePart):
    """Class that represents a Fuse Box.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Fuse_Box)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 4, 1)

@dataclass
class TubesShort(BasePart):
    """Class that represents a Tubes Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tubes_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class TubesLong(BasePart):
    """Class that represents a Tubes Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tubes_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 4, 2)

@dataclass
class TubesCorner(BasePart):
    """Class that represents a Tubes Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tubes_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class TubesJoin(BasePart):
    """Class that represents a Tubes Join.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Tubes_Join)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(2, 2, 2)

@dataclass
class SmallPipeShort(BasePart):
    """Class that represents a Small Pipe Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeLong(BasePart):
    """Class that represents a Small Pipe Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 1, 1)

@dataclass
class SmallPipeBend(BasePart):
    """Class that represents a Small Pipe Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeTee(BasePart):
    """Class that represents a Small Pipe Tee.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Tee)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeCorner(BasePart):
    """Class that represents a Small Pipe Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeFourWay(BasePart):
    """Class that represents a Small Pipe Four Way.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Four_Way)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeFourWayTee(BasePart):
    """Class that represents a Small Pipe Four Way Tee.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Four_Way_Tee)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeFiveWay(BasePart):
    """Class that represents a Small Pipe Five Way.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Five_Way)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class SmallPipeSixWay(BasePart):
    """Class that represents a Small Pipe Six Way.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Small_Pipe_Six_Way)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargePipeMount(BasePart):
    """Class that represents a Large Pipe Mount.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Mount)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class HolderSupportLegBase(BasePart):
    """Class that represents a Holder Support Leg Base.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Holder_Support_Leg_Base)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class HolderSupportLeg(BasePart):
    """Class that represents a Holder Support Leg.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Holder_Support_Leg)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class HolderSupportBend(BasePart):
    """Class that represents a Holder Support Bend.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Holder_Support_Bend)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class LargePipeExtension(BasePart):
    """Class that represents a Large Pipe Extension.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Extension)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class LargePipeCap(BasePart):
    """Class that represents a Large Pipe Cap.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Cap)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 1, 3)

@dataclass
class LargePipeCompressor(BasePart):
    """Class that represents a Large Pipe Compressor.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Large_Pipe_Compressor)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(5, 5, 8)

@dataclass
class PowerStation(BasePart):
    """Class that represents a Power Station.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Power_Station)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(4, 7, 2)

@dataclass
class GiantPipe(BasePart):
    """Class that represents a Giant Pipe.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 8, 7)

@dataclass
class GiantPipeGlassStraight(BasePart):
    """Class that represents a Giant Pipe Glass Straight.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Glass_Straight)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 8, 7)

@dataclass
class GiantPipeCorner(BasePart):
    """Class that represents a Giant Pipe Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 7, 7)

@dataclass
class GiantPipeGlassCorner(BasePart):
    """Class that represents a Giant Pipe Glass Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Glass_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 7, 7)

@dataclass
class GiantPipeTee(BasePart):
    """Class that represents a Giant Pipe Tee.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Tee)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 7, 7)

@dataclass
class GiantPipeBracer(BasePart):
    """Class that represents a Giant Pipe Bracer.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Bracer)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 1, 7)

@dataclass
class GiantPipeHolder(BasePart):
    """Class that represents a Giant Pipe Holder.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Giant_Pipe_Holder)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(7, 2, 8)

@dataclass
class WarehouseVentilationShort(BasePart):
    """Class that represents a Warehouse Ventilation Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class WarehouseVentilationLong(BasePart):
    """Class that represents a Warehouse Ventilation Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 6)

@dataclass
class WarehouseVentilationCorner(BasePart):
    """Class that represents a Warehouse Ventilation Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class WarehouseVentilationTee(BasePart):
    """Class that represents a Warehouse Ventilation Tee.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Tee)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 3)

@dataclass
class WarehouseVentilationMount(BasePart):
    """Class that represents a Warehouse Ventilation Mount.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Mount)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(3, 3, 1)

@dataclass
class WarehouseVentilationDrum(BasePart):
    """Class that represents a Warehouse Ventilation Drum.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Warehouse_Ventilation_Drum)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(8, 6, 5)

@dataclass
class GeneratorPipeShort(BasePart):
    """Class that represents a Generator Pipe Short.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Short)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class GeneratorPipeLong(BasePart):
    """Class that represents a Generator Pipe Long.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Long)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 3, 1)

@dataclass
class GeneratorPipeCorner(BasePart):
    """Class that represents a Generator Pipe Corner.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Corner)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class GeneratorPipeTee(BasePart):
    """Class that represents a Generator Pipe Tee.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Tee)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)

@dataclass
class GeneratorPipeFourWay(BasePart):
    """Class that represents a Generator Pipe Four Way.
    """
    shapeId: str = field(kw_only=True, default=SHAPEID.Generator_Pipe_Four_Way)

    def __post_init__(self):
        super().__post_init__()
        self._box = vec3(1, 1, 1)