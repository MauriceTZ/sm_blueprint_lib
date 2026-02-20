from dataclasses import dataclass, field

from .baseinteractablepart import BaseInteractablePart
from ..controllers.totebotheadcontroller import TotebotHeadController


@dataclass
class BaseTotebotHeadPart(BaseInteractablePart):
    """Base class for Totebot Heads.
    """
    controller: TotebotHeadController = field(default_factory=TotebotHeadController)

    def __post_init__(self):
        if not isinstance(self.controller, TotebotHeadController):
            try:
                self.controller = TotebotHeadController(**self.controller)
            except TypeError:
                self.controller = TotebotHeadController(*self.controller)
        super().__post_init__()
