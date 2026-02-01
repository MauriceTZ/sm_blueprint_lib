from dataclasses import dataclass, field

from .baseinteractablepart import BaseInteractablePart
from ..controllers import BaseLogicController
from ...id import *

@dataclass
class BaseLogicPart(BaseInteractablePart):
    """Base class for Logic parts with active state (mostly Logic Gate and Timer)
    """
    controller: BaseLogicController = field(default_factory=BaseLogicController)

    def __post_init__(self):
        if not isinstance(self.controller, BaseLogicController):
            self.controller = BaseLogicController(**self.controller)
        super().__post_init__()
