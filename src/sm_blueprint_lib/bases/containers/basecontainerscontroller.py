from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ..controllers.basecontroller import *
from .basecontainer import *


@dataclass
class BaseContainersController(BaseController):
    """Base class for Controllers that have a "containers" attribute.
    """
    containers: Optional[list[BaseContainer]] = field(kw_only=True, default=None)

    def __post_init__(self):
        if self.containers:
            self.containers = [BaseContainer(**c)
                               if not isinstance(c, BaseContainer) else
                               c
                               for c in self.containers]
        super().__post_init__()
