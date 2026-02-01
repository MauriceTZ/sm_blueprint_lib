from dataclasses import dataclass, field

from .basecontroller import BaseController


@dataclass
class GearController(BaseController):
    gear: int
