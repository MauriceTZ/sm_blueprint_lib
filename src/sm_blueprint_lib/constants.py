class SHAPEID:
    """Shape ID constants for Blocks and Parts.
    """
    BARRIER_BLOCK = "09ca2713-28ee-4119-9622-e85490034758"
    LOGIC_GATE = "9f0f56e8-2c31-4d83-996c-d00a9b296c3f"
    TIMER = "8f7fd0e7-c46e-4944-a414-7ce2437bb30f"
    SENSOR5 = "20dcd41c-0a11-4668-9b00-97f278ce21af"
    SWITCH = "7cf717d7-d167-4f2d-a6e7-6b2c70aa3986"
    BUTTON = "1e8d93a4-506b-470d-9ada-9c0a321e2db5"

    SPORT_SUSPENSION5 = "52855106-a95c-4427-9970-3f227109b66d"
    OFFROAD_SUSPENSION5 = "73f838db-783e-4a41-bc0f-9008967780f3"
    BEARING = "4a1b886b-913e-4aad-b5b6-6e41b0db23a6"
    PISTON5 = "2f004fdf-bfb0-46f3-a7ac-7711100bee0c"
    SHAPEID_TO_CLASS = {}
    JOINT_TO_CLASS = {}


class COLOR:
    """Color constants for Blocks and Parts.
    """
    DEFAULT_BARRIER_BLOCK = "CE9E0C"
    DEFAULT_BUTTON = "DF7F01"
    DEFAULT_LOGIC_GATE = "DF7F01"
    DEFAULT_SENSOR5 = "DF7F01"
    DEFAULT_SWITCH = "DF7F01"
    DEFAULT_TIMER = "DF7F01"


class AXIS:
    """Default axises
    """
    DEFAULT_XAXIS = 1
    DEFAULT_ZAXIS = 3
    DEFAULT_XAXIS_INTERACTABLE = 1
    DEFAULT_ZAXIS_INTERACTABLE = -2


class VERSION:
    """Blueprint version
    """
    BLUEPRINT_VERSION = 4


TICKS_PER_SECOND = 40

__global_id_counter = 0
"""Atempting to modify this global variable may cause to break your blueprints lol.
"""


def get_new_id():
    """Get a unique ID (incremental)

    Returns:
        int: The unique ID.
    """
    global __global_id_counter
    __global_id_counter = (new_id := __global_id_counter) + 1
    return new_id
