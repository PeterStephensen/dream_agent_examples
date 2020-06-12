from dream_agent import Agent
#----------------------------------------------------------------
# In this tutorial we will learn:
# 1) To make a new object that is 'inherited' from the Agent object
# 2) To add new 'properties' to this object
# 3) To program how this new object reacts on different 'events' (the event_proc)
# 4) As part of this we will learn how to 'override' a method in python
#----------------------------------------------------------------

# We would like to define a new object (called Person) that:
# 1) Can do all the same things as an Agent
# 2) Has the extra properties 'name' and 'age'.

# We define the new class like this:

class Person(Agent):                                  #1

    # Overriding the constructor
    def __init__(self, parent=None, name="", age=0):  #2
        super().__init__(parent)                      #3 Calls the base constructor
        self._name = name                             #4
        self._age = age                               #5

    # Report name
    def get_name(self):                               #6
        return self._name

    # Report age
    def get_age(self):                                #7
        return self._age


# In the first line (#1) we define that Person is 'inherited' from Agent. That implies that all the
# methods and fields decribed in the last section automatically are avaiable.

# An object (also called a class) has a 'constructor'. The constructor is called when the object is allocated.
# In python the constructor is a method with the name __init__. If you look in dream_agent.py you will see the
# constructor defined as:
#    def __init__(self, parent=None):
# The constructor has a parent object as argument, but this object defaults to None (no object).
# We can therefore write both:
#    p = Agent()
# and
#    p = Agent(p1)
# where p1 is the parent object. If we write nothing, python knows that parent defaults to None.

# We are going to 'override' the constructor (#2). This is done by adding our own __init__ function with extra arguments name and age.
# Observe that name defaults to "" and age defaults to 0. The extra arguments have to have default values or you will get an error.

# In the second line of the constructor (#3) the base implementation of the Agent constructor is called. This is important as we still
# wants the basic behavior of the Agent class to apply.

# In #4 and #5 the internal representations self._name and self._age of the properties name and age are defined. In python an underscore
# signals that a variable is private and should not be used outside the class.

# To get access to name and age from the outside, the two get-properties get_name and get_age are defined in #5 and #6

# Now let us use the new class
population = Agent()
Person(parent=population, name="Joe", age=14)
Person(parent=population, name="Peter", age= 33)
Person(parent=population, name="Paul", age= 37)

for p in population:
    print(p.get_name())

#----------------------------------------------------------------
# The event_proc
#----------------------------------------------------------------

# We can now make our first agent based model. The model runs like this:
# 1. Joe, Peter and Paul are added to the model
# 2. The model runs for 20 years
# 3. Everybody reports their name and age

# We start by defining the 'events' of the model:
class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.update = 3        # Agents behavior

# We define the Person class and overrides the event_proc. The base implementation of event_proc is to
# input id_event and then send the id_event to all the childrens event_proc's (if any children). This is the
# basic architecture of models build with the Agent class. The agents forms at tree and events are send down the tree.

# The new event_proc starts at #1. If the person recieves a Event.update the age is increased with 1 year (#2).
# If the person recieves a Event.stop the name and age is reported (#3).
# Observe that the base implementation of event_proc (sendig id_event to all children) is given by
# super().event_proc(id_event) (#4). It is not relevant in this simple model.
class Person(Agent):

    # Overriding the constructor
    def __init__(self, parent=None, name="", age=0):
        super().__init__(parent)
        self._name = name
        self._age = age

    # Overriding event_proc
    def event_proc(self, id_event):                                   #1
        if id_event == Event.update:                                  #2
            self._age += 1
        elif id_event == Event.stop:                                  #3
            print("Name: {}, Age: {}".format(self._name,self._age))
        else:                                                         #4
            super().event_proc(id_event) # Base implementation: Send to children

    # Report name
    def get_name(self):
        return self._name

    # Report age
    def get_age(self):
        return self._age


# We can now run the model
#--------------------------

# Define the population
population = Agent()

# Add persons to the population
Person(parent=population, name="Joe", age=14)
Person(parent=population, name="Peter", age= 33)
Person(parent=population, name="Paul", age= 37)

# All agents can initialize (not relevant in this example)
population.event_proc(Event.start)

# Run for 20 years
for t in range(20):
    print("Time: ",t)
    population.event_proc(Event.update)  # The population object will automatically send the event to the children

# All agents can clean up
population.event_proc(Event.stop)


