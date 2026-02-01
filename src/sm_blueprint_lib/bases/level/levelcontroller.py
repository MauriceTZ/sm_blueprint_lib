from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ..controllers.basecontroller import *


@dataclass
class BaseLevelController(BaseController):
    """Base class for Controllers that have a "level" attribute.
    """
    level: int
