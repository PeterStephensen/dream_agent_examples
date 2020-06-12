#-------------------------------------------------------------------
# In this first tutorial we will play around with the Agent object
#-------------------------------------------------------------------
# We need to import the implementation of Agent
from dream_agent import Agent

# We allocate an agent object...
p = Agent()

# ..and adds 4 agent objects to p.
child1 = Agent()
child2 = Agent()
child3 = Agent()
child4 = Agent()

p.add_agent(child1)
p.add_agent(child2)
p.add_agent(child3)
p.add_agent(child4)
# child1,.., child4 are called p's child objects
# p is the parent object
# The agents forms a tree

# We can add child objects to the child objects
child5 = Agent()
child6 = Agent()
child4.add_agent(child5)
child4.add_agent(child6)
# Agent child6 is a child of child4 and a descentant of agent p.
# Agent p is an ancestor of all the other agents

# We can report the number of child objects in p...
print("Number of agents in p:", p.get_number_of_agents())

#.. and the total number of agents at run-time
print("Total number of agents:", Agent.get_total_number_of_agents())

# We can do stuff to all child objects:
for c in p:
    print(c.get_id())

print("----------------------")

# We can randomize children
p.randomize_agents()

for c in p:
    print(c.get_id())

# We can remove the child objects
p.remove_agent(child1)
p.remove_agent(child2)
p.remove_agent(child3)
p.remove_agent(child4)

# Now there is 0 agents in p
print("Now there is 0 agents in p:", p.get_number_of_agents())

# A faster way to add agents to p is this:
child1 = Agent(p)
child2 = Agent(p)

# Now there are 2 agents in p
print("Now there are 2 agents in p:", p.get_number_of_agents())

# Add 500 agents
for i in range(500):
    p.add_agent(Agent())

# Add 500 more (less code)
for i in range(500):
    Agent(p)

# Now there are 1002 agents in p
print("Now there are 1002 agents in p:", p.get_number_of_agents())

#.. and the total number of agents
print("Total number of agents:", Agent.get_total_number_of_agents())

#----------------------------------------------------------------
# An agent object p has 10 methods:
#----------------------------------------------------------------
# p.remove_agent(c)           Remove child c
# p.get_number_of_agents()    Report number of child objects
# p.count()                   The same as get_number_of_agents()
# p.add_agent(c)              Add agent c as a child
# p.randomize_agents()        Randomize the list of child agents
# p.get random_agents()       Returns 1 or more random child objects
# p.get_id()                  The unique id of the agent
# p.remove_this_agent()       The agent can remove it self from its parent
# p.event_proc(id_event)      Method that defines the behavior of the agent
#----------------------------------------------------------------
# Fields:
#----------------------------------------------------------------
# p.remove_when_empty         If True, the parent is removed if all its child objects are removed
# p.removed                   Is True if it has been removed
#----------------------------------------------------------------
# Static methods:
#----------------------------------------------------------------
# Agent.get_total_number_of_agents()  Total number of agents at run-time






