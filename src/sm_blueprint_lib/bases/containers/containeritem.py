from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ...bases import *


@dataclass
class ContainerItem:
    """Class for Items inside a Container.
    """
    quantity: int
    uuid: str
