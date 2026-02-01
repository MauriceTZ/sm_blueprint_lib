from dataclasses import dataclass, field
from typing import Any, Optional

from ...constants import get_new_id
from ...id import ID
from .basecontroller import *

@dataclass
class LightController(BaseController):
    """Base controller class for light objects
    """
    color: str
    coneAngle: int
    luminance: int
