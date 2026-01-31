from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ...bases import *


@dataclass
class UUIDFilter:
    """Class for UUID filters inside a Container.
    """
    uuid: str
