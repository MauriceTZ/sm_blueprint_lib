from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from ..controllers.basecontroller import *


@dataclass
class BaseDataController(BaseController):
    """Base class for controller objects that have a "data" attribute.
    """
    data: str
