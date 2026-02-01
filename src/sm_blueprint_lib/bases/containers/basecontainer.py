from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from .containeritem import *
from .uuidfilter import *

@dataclass
class BaseContainer:
    """Base class for Containers.
    """
    container: list[ContainerItem]
    filters: list[UUIDFilter]
    id: int
    slots: int
    stackSize: int

    def __post_init__(self):
        self.container = [ContainerItem(**c)
                            if not isinstance(c, ContainerItem) else
                            c
                            for c in self.container]
        self.filters = [UUIDFilter(**f)
                        if not isinstance(f, UUIDFilter) else
                        f
                        for f in self.filters]