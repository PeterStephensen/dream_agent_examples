from enum import Enum

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period. Statistics makes statistics
    PERIOD_STOP = 3   # The end of a period. Agents calculate utility and profits
    UPDATE = 4        # Stuff that happens in the period

# Communication
#---------------------------
class ECommunication(Enum):
    YES = 1         
    NO = 2         
    OK = 3
    HI = 4
