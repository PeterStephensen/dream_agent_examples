# Peter Stephensen, DREAM 2019
import sys, os
sys.path.append(os.getcwd()) # Add root-dir to sys.path

from dream_agent import Agent
import random

#----------------------------------------------------------------
# In this tutorial we make the first full model. It will be a simple demographic microsimulation model.
# A microsimulation model is an agent based model without agent interaction.
# In each period a constant number of persons are born. Each person dies with a constant probability.
# We will learn to:
# 1) Make a Simulation object that controls the simulation
# 2) Make a Settings object that contains parameters that the user should choose
#----------------------------------------------------------------

#--------------------------------------------------
# We start by defining the 'events' of the model:
#--------------------------------------------------
class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.update = 3        # Agent behavior

# All agents will receive these events and can react on them.
# On Event.update the agent should express its behavior (consume, produce, look for work, die ect.)

#--------------------------------------------------
# The Settings-object
#--------------------------------------------------
# The Settings-object contains all informations that the user should supply
# All elements should be given a default value.
class Settings: pass
Settings.number_of_agents=0
Settings.number_of_periods=0
Settings.probability_of_death=0
Settings.number_of_new_born=0

#--------------------------------------------------
# The Person-object
#--------------------------------------------------
# When the person is born the age is 0 (#1)
# In the event_proc the person reacts on Event.update (#2).
# The persons behavior:
# 1) get 1 year older (#3)
# 2) or die (#4)
# Observe that the agent can self-destruct with self.remove_this_agent().
# The person will automatically be removed from the population.
class Person(Agent):

    # Constructor
    def __init__(self, parent=None):
        super().__init__(parent)
        self._age = 0                                           #1

    def event_proc(self, id_event):
        if id_event == Event.update:                            #2
            self._age += 1                                      #3
            if random.random() < Settings.probability_of_death:
                self.remove_this_agent()                        #4

    def get_age(self):
        return self._age


#--------------------------------------------------
# The Simulation-object
#--------------------------------------------------
# This is the object that runs the model.
# The object has two so-called static fields (#1). You can think about these fields
# as global fields. All other objects can get access to the population and time
# by using Simulation.population and Simulation.time.
#
# All the models initial agents are allocated in the constructor (#2)
# The Simulation object has 1 child: the population (#3)
# Persons are added to the population (#4)
# Finally the constructor starts the model by sending a Event.start to itself,
# and thereby to all its descendants (#5)
#
# In the event_proc the Simulation object reacts on Event.start (#6)
# First it sends the Event.start to all its descendants (#7)
# Then it starts the co-called 'Event-Pump'. Here events are pumped down the agent-tree
# in a sequence that defines the specific functioning of the model. In this simple model
# Event.update is the only event that is executed every periode.
# Every round the time counts up one unit and the number of persons are written to the console.
#
# The Simulation object also reacts on Event.update by allocating new born persons (#10)

class Simulation(Agent):
    # Static fields
    population = Agent()                                 #1
    time = 0

    # Constructor
    def __init__(self):                                  #2
        super().__init__()
        # Initial allocation of all agents

        # Simulation has 1 child:
        Simulation.population = Agent(self)              #3

        # Adding persons to the population
        for i in range(Settings.number_of_agents):       #4
            Person(Simulation.population)

        # Start the simulation
        self.event_proc(Event.start)                     #5

    def event_proc(self, id_event):
        if id_event == Event.start:                      #6
            # Send Event.start down the tree to all decendants
            super().event_proc(id_event)                 #7

            # The Event Pump: the actual simulation      #8
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.update)
                Simulation.time += 1
                print(Simulation.population.get_number_of_agents())

            # Stop the simulation
            self.event_proc(Event.stop)                  #9


        elif id_event == Event.update:                   #10
            # Adding new born persons to the population
            for i in range(Settings.number_of_new_born):
                Person(Simulation.population)
            super().event_proc(id_event)
        else:
            # All other events are sendt to decendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------

Settings.number_of_agents = 100
Settings.number_of_periods = 1000
Settings.probability_of_death = 0.01
Settings.number_of_new_born = 5

Simulation()

