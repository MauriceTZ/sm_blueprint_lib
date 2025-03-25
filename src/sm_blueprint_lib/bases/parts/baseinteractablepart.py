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

    def connect(self, o: "BaseInteractablePart"):
        if not self.controller.controllers:
            self.controller.controllers = []
            
        self.controller.controllers.append(ID(o.controller.id))
        return o
