from dataclasses import dataclass, field
from pprint import pp

from .bases.parts.basepart import BasePart
from .constants import SHAPEID


@dataclass
class Body:
    """Class that represents a Body inside a Blueprint, each Joint defines a new Body.
    """
    childs: list[BasePart] = field(default_factory=list)

    def __post_init__(self):
        try:
            c = None
            self.childs = [SHAPEID.SHAPEID_TO_CLASS[child["shapeId"]](**child)
                        if not isinstance((c:=child), BasePart) else
                        child
                        # Exclude not supported parts
                        for child in self.childs if SHAPEID.SHAPEID_TO_CLASS.get(child["shapeId"])]
        except Exception as e:
            pp(c)
            print(SHAPEID.SHAPEID_TO_CLASS[c["shapeId"]].__name__)
            raise e
        