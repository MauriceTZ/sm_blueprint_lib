"""
# sm_blueprint_lib
Yeah we definitely need a better description.
"""

from .blueprint import *
from .body import *
from .bounds import *
from .constants import *
from .id import *
from .pos import *
from .utils import *

from .parts import *
from .prebuilds import * # imports changed so this doesnt work anymore...
from .rot import *
from .bases import *
from .blocks import *

# The 3D preview module pulls in pygame / moderngl / imgui. Make it optional
# so headless use cases (e.g. running the simulator in CI) don't require the
# graphics stack to be installed.
try:
    from .preview import *
except ImportError:
    pass

from .simulator import Simulator, MutualGateConnectionError