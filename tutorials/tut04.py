# Peter Stephensen, DREAM 2019
import sys, os
sys.path.append(os.getcwd()) # Add root-dir to sys.path

from dream_agent import Agent
import random

#----------------------------------------------------------------
# In this tutorial we add a Statistics object to the model
# This is a 'statistics department' that gathers data from the model.
# In this example the Statistics object gathers aggergated information an write to a text file
#----------------------------------------------------------------

# We start by defining the 'events' of the model:
class Event: pass
Event.start = 1         # The model starts
Event.stop = 2          # The model stops
Event.period_start = 3  # The start of a period
Event.update = 4        # Stuff that happens in the periode

# Stock-flow-considerations
#---------------------------
# Observe we have a new event called 'period_start'.
# Event.update is what happenes during the periode (death, consume, look for job ect.).
# This is the flows of the model. This is where agents 'do' stuff.
# Event.period_start is when agents count their stocks. This is where agents consolidates, plans and counts.
# And where the Statistics object gathers primo data

# The Settings object
#---------------------------
class Settings: pass
Settings.number_of_agents = 0
Settings.number_of_periods = 0
Settings.probability_of_death = -1
Settings.number_of_new_born=0
Settings.out_file=""

# The Person object
#---------------------------
class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._age = 0

    def event_proc(self, id_event):
        if id_event == Event.update:
            self._age += 1
            if random.random() < Settings.probability_of_death:
                self.remove_this_agent()

    def get_age(self):
        return self._age


#---------------------------
# The Statistics object
#---------------------------
# The Statistics object overrides the event_proc method.
# When the model starts it opens a text file (#1)
# When the model stops it closes the file (#2)
# At the start of all periodes (Event.period_start) the number of persons are written to the file
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.start:                     #1
            self._file = open(Settings.out_file, "w")

        elif id_event == Event.stop:                    #2
            self._file.close()

        elif id_event == Event.period_start:            #3
            print(Simulation.population.get_number_of_agents())
            self._file.write("{}\t{}\n".format(Simulation.time, Simulation.population.get_number_of_agents()))



#---------------------------
# The Simulation object
#---------------------------
# The Simulation object now have 2 children: population and _statistics (#1)
# Events will automatically be send to the Statistics object
# The Event Pump (#2) do not write to the console like in the last section.
# Reporting of data is a job for the Statistics object.

class Simulation(Agent):
    # Static fields                   # A kind of global objects. All other objects can read time from Simulation.time
    population = Agent()              # and population from Simulation.population
    time = 0

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents

        # Simulation has two children:
        self._statistics = Statistics(self)           #1
        Simulation.population = Agent(self)

        # Adding persons to the population
        for i in range(Settings.number_of_agents):
            Person(Simulation.population)

        # Start the simulation
        self.event_proc(Event.start)

    def event_proc(self, id_event):
        if id_event == Event.start:
            # Send Event.start down the tree to all decendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation   #2
            while Simulation.time < Settings.number_of_periods:
                self.event_proc(Event.period_start)
                self.event_proc(Event.update)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.stop)

        elif id_event == Event.update:
            # Adding new born persons to the population
            for i in range(Settings.number_of_new_born):
                Person(Simulation.population)
            super().event_proc(id_event)
        else:
            # All other events are sendt to decendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------

Settings.number_of_agents = 500
Settings.number_of_periods = 1000
Settings.probability_of_death = 0.01
Settings.number_of_new_born = 5
Settings.out_file = "test.txt"

Simulation()

# You can find output from the simulation in test.txt
# Do not write too much to files. It is very time consuming.
