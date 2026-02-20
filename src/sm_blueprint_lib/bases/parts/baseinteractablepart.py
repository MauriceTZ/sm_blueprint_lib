from dataclasses import dataclass, field

from ..controllers.basecontroller import BaseController
from .basepart import BasePart
from ...id import ID
from ...constants import AXIS


@dataclass
class BaseInteractablePart(BasePart):
    """Base class for Interactable parts
    """
    controller: BaseController = field(default_factory=BaseController)
    xaxis: int = field(kw_only=True, default=AXIS.DEFAULT_XAXIS_INTERACTABLE)
    zaxis: int = field(kw_only=True, default=AXIS.DEFAULT_ZAXIS_INTERACTABLE)

    def __post_init__(self):
        if not isinstance(self.controller, BaseController):
            self.controller = BaseController(**self.controller)
        super().__post_init__()

    def connect(self, o):
        if not self.controller.controllers:
            self.controller.controllers = []
        if type(o) is int:
            if ID(o) in self.controller.controllers:
                raise ValueError(f"You are connecting two objects twice: {self} and {ID(o)}")
            self.controller.controllers.append(ID(o))
            return o

        if ID(o.controller.id) in self.controller.controllers:
            raise ValueError(f"You are connecting two objects twice: {self} and {o}")
        self.controller.controllers.append(ID(o.controller.id))
        return o

    def disconnect(self, o):
        if not self.controller.controllers:
            self.controller.controllers = []
        if ID(o.controller.id) not in self.controller.controllers:
            raise ValueError(f"You are trying to disconnect this two unconnected objects: {self} and {o}")
        self.controller.controllers.remove(ID(o.controller.id))
        return o
