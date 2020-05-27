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
    DO_YOU_HAVE_A_JOB = 0 
    I_QUIT = 1
    YES = 2         
    NO = 3         
    OK = 4
