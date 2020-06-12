import random
import math
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum

from dream_agent import Agent

#----------------------------------------------------------------
# In this tutorial we add agent interaction: You will learn:
# 1) How an agent do a random search
# 2) How agents communicate
# 3) How agents transfers money
# 4) Showing a histogram
#----------------------------------------------------------------
# We model a system of persons that randomly attack each other(!). Each person has a normally distributed 'strength'.
# You do not know the strength of your opponent when you attack. The strongest win and the looser pays a share
# of his wealth to the winner. We show a real-time-histogram of the wealth distribution.

# Communication protocol (described later)
#---------------------------
class ECommunication(Enum):
    YOU_WIN = 1
    YOU_LOSE = 2
    I_ATTACK = 3

class Event(Enum):
    START = 1         # The model starts
    STOP = 2          # The model stops
    PERIOD_START = 3  # The start of a period
    UPDATE = 4        # Stuff that happens in the period

# The Settings object
#---------------------------
class Settings(): 
    number_of_agents = 1000
    number_of_periods = 10000
    out_file = "test.txt"

    graphics_show = True
    graphics_periods_per_pic = 15

    loot_share = 0.25 # If you win, this is the share of the others wealth you get
    attack_probability = 0.1

# The Person object
#---------------------------
# #1) Everybody starts with 1 unit of wealth (equal wealth distribution) and normally distributed strength

# #2) At Event.update the person attacks a random other person with probability Settings.attack_probability.
# The person uses the method Simulation.population.get_random_agent(self) to do a random search. It is important to
# use self as an argument to make sure that the person do not find itself in the search.
# The person sends the message ECommunication.I_attack to the random person p. Person p responds with
# ECommunication.you_win or ECommunication.you_lose (see later). If the reply is ECommunication.you_lose, the person has
# to pay a share Settings.loot_share of its wealth to the person p. This is done with the transfer_to-method (see later)

# #3) The communicate-method is the basic way to model interaction. This and the enumeration ECommunicate defines
# the communication protocol. ECommunicate is the 'language' used by the agents, and the communicate-method defines the
# Q&A-structure. You contact a person by using her communicate-method, and her answer is what the communication-method returns.
# If a person receives the message ECommunication.I_attack it can return ECommunication.you_win or ECommunication.you_lose.
# If the sender of the message is stronger than you (if self._strength < person._strength), you transfer money to the sender and
# returns ECommunication.you_win. If you are stronger yor return ECommunication.you_lose (the sender then transfers money to you).

# #4) Transferring money between two agents is an action that has simultaneous impact on both agents. This is best
# modelled by a single method. If you are transferring money to another person, money are subtracted from your
# wealth and added to the other persons wealth. That is what happens in the transfer_to-method.
class Person(Agent):

    def __init__(self, parent=None):
        super().__init__(parent)
        self._wealth = 1                                        #1
        self._strength = random.gauss(0,1)

    def event_proc(self, id_event):
        if id_event == Event.UPDATE:
            if random.random() < Settings.attack_probability:   #2
                # Random search
                p = Simulation.population.get_random_agent(self)
                # Communication
                if (p.communicate(ECommunication.I_ATTACK, self) == ECommunication.YOU_LOSE):
                    self.transfer_to(p, Settings.loot_share * self._wealth)

    def communicate(self, communication, person):                #3
        if communication == ECommunication.I_ATTACK:
            if self._strength < person._strength:
                self.transfer_to(person, Settings.loot_share * self._wealth)
                return ECommunication.YOU_WIN
            else:
                return ECommunication.YOU_LOSE

    def transfer_to(self, other, value):                       #4
        self._wealth -= value
        other._wealth += value

    def get_wealth(self):
        return self._wealth

# The Statistics object
#---------------------------
class Statistics(Agent):

    def event_proc(self, id_event):
        if id_event == Event.START:
            self._file = open(Settings.out_file, "w") # Not used

            # Initialize graphics
            if Settings.graphics_show:
                plt.ion()
                plt.figure(figsize=[5,5])

        elif id_event == Event.STOP:
            self._file.close()  # Not used

        elif id_event == Event.PERIOD_START:
            print(Simulation.time)

            if Settings.graphics_show:
                if Simulation.time % Settings.graphics_periods_per_pic==0:
                    # Gather data from population
                    w = []
                    for p in Simulation.population:
                        w.append(math.log(p.get_wealth()))

                    # Display data
                    plt.clf()
                    plt.hist(w, bins=50, color="blue")
                    plt.axis(ymin=0, ymax=100)
                    plt.title("Distribution of log-wealth ({})".format(Simulation.time))
                    plt.show()
                    plt.pause(0.000001)
                    #3

# The Simulation object
#---------------------------
# #1) We add Simulation.population.randomize_agents() to the Event Pump. The agents are shuffled
# every period to ensure randomness when the agents do random search with the method
# Simulation.population.get_random_agent(self).
class Simulation(Agent):
    # Static fields
    population = Agent()
    time = 0

    def __init__(self):
        super().__init__()
        # Initial allocation of all agents

        # Simulation has two children:
        self._statistics = Statistics(self)
        Simulation.population = Agent(self)

        # Adding persons to the population
        for _ in range(Settings.number_of_agents):
            Person(Simulation.population)

        # Start the simulation
        self.event_proc(Event.START)

    def event_proc(self, id_event):
        if id_event == Event.START:
            # Send Event.start down the tree to all defendants
            super().event_proc(id_event)

            # The Event Pump: the actual simulation
            while Simulation.time < Settings.number_of_periods:
                # Important when agents are searching
                Simulation.population.randomize_agents()                #1
                self.event_proc(Event.PERIOD_START)
                self.event_proc(Event.UPDATE)
                Simulation.time += 1

            # Stop the simulation
            self.event_proc(Event.STOP)

        else:
            # All other events are send to defendants
            super().event_proc(id_event)


# We can now run the model
#--------------------------

Simulation()

