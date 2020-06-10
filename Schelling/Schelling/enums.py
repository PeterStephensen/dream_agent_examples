from enum import Enum

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period
    UPDATE = 3        # Stuff that happens in the period

# Agent types
#---------------------------
class EType(Enum):
    MAJORITY = 0
    MINORITY = 1
