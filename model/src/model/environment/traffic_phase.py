from enum import Enum

class TrafficPhase(Enum):
    NORTH_SOUTH_GREEN = 0
    NORTH_SOUTH_YELLOW = 1
    EAST_WEST_GREEN = 2
    EAST_WEST_YELLOW = 3
    ALL_RED = 4
    TRANSITION = 5