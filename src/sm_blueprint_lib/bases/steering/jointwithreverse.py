from dataclasses import dataclass

from ...id import ID


@dataclass
class JointWithReverse(ID):
    reverse: int