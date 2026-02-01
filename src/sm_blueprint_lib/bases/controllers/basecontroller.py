from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID


@dataclass
class BaseController:
    """Base class for controller objects (used in interactable parts and so)
    """
    controllers: Optional[list[ID]] = field(kw_only=True, default=None)
    id: int = field(kw_only=True, default_factory=get_new_id)
    joints: Optional[list[ID]] = field(kw_only=True, default=None)

    def __post_init__(self):
        if self.controllers:
            self.controllers = [ID(**c)
                                if not isinstance(c, ID) else
                                c for c in self.controllers]
        if self.joints:
            self.joints = [ID(**jj)
                           if not isinstance(jj, ID) else
                           jj for jj in self.joints]
