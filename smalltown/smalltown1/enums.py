from enum import Enum

# Events
#---------------------------
class Event(Enum):
    START = 0         # The model starts
    STOP = 1          # The model stops
    PERIOD_START = 2  # The start of a period. Statistics makes statistics. Initialize flow-counters
    UPDATE = 3        # Stuff that happens in the period
    PERIOD_STOP = 4   # The end of a period. Agents calculate utility and profits. Sum up the flows

# Communication
#---------------------------
class ECommunication(Enum):
    YES=1         
    NO=2         
    OK=3
    HI=4
    DO_YOU_HAVE_A_JOB=5
    I_QUIT=6
    YOU_ARE_FIRED=7


    
