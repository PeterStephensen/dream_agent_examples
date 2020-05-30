import random
import sys
import numpy as np

class Agent:
    """Class used for agent based modelling and microsimulation
    """
    _nAgents = 0

    def __init__(self, parent=None):
        """Constructor for the Agent class

        Keyword Arguments:
            parent {Agent} -- The parent object (default: {None})
        """
        self._id = Agent._nAgents
        Agent._nAgents += 1
        self._first, self._next = None, None
        self._prev, self._last = None, None
        self._parent, self._a_itt = None, None
        self._count = 0
        self.removed, self.remove_when_empty = False, False
        self._random_agent=None
        
        if parent is not None: 
            parent.add_agent(self)

    def event_proc(self, id_event):
        """This method describes the behavior of the agent

        Arguments:
            id_event {Enum} -- An id that identifies the event that the agent experiences
        """
        for a in self:
            a.event_proc(id_event)
        
        if self.remove_when_empty and self._count==0:
            self.remove_this_agent()

    def add_agent(self, a):
        """Add new child agent

        Arguments:
            a {Agent} -- The new child agent
        """
        if not isinstance(a, Agent):
            raise SystemExit('Error: Argument a in add_agent should be Agent.')
        
        # Release old relations
        a.remove_this_agent()

        # Create new relations
        a._prev, a._next = self._last, None
        a._parent = self
    
        if self._first is None:
            self._first = a
        else:
            self._last._next = a

        self._last = a
        self._count += 1


    def remove_agent(self, a):
        """Remove a child agent

        Arguments:
            a {Agent} -- The child agent that should be removed
        """
        if not isinstance(a, Agent):
            raise SystemExit('Error: Argument a in remove_agent should be Agent.')

        self.removed = True

        if self._count==1:
            self._first, self._last = None, None
        else:
            if a._prev is not None: a._prev._next = a._next
            if a._next is not None: a._next._prev = a._prev
            
            if a == self._first: self._first = a._next
            if a == self._last: self._last = a._prev

        self._count -= 1


    def remove_this_agent(self):
        """Removes this agent from it's connection to the parent agent. The agent ceases to exit.
        """
        if self._parent != None:
            self._parent.remove_agent(self)

    def randomize_agents(self):
        """The order of the child agents are randomized.
        """
        if self._count>1:
            lst = []
            for a in self: lst.append(a)
            random.shuffle(lst)
            self._first, self._last = lst[0], lst[-1]
            lst[0]._prev, lst[0]._next = None, lst[1]
            lst[-1]._prev, lst[-1]._next = lst[-2], None
            if self._count>2:
                for i in range(1,self._count-1):
                    lst[i]._prev, lst[i]._next = lst[i-1], lst[i+1]


    def get_random_agents(self, not_this_agent=None, n=1):
        """Generates a list of random child agents

        Keyword Arguments:
            not_this_agent {Agent} -- An agent not to return. Will often be 'this'.  (default: {None})
            n {int} -- Number of agents to return. If the number of agents is less than n, all agents are returned.  (default: {1})

        Returns:
            Agent -- A list of random agents. Returns None if no children
        """
        
        if (not (not_this_agent is None)) and (not isinstance(not_this_agent, bool)):
            raise SystemExit('Error: Argument not_this_agent in get_random_agent should be None or bool.')

        if not isinstance(n, int):
            raise SystemExit('Error: Argument n in get_random_agent should be int.')
        
        # If no children: end here
        if self._first is None:    
            return None

        # If _random_agent not initialized: initialize
        if self._random_agent == None:  
            self.randomize_agents() # Start by randomizing            
            self._random_agent = self._first

        # If n larger than the number of agents: use the agents available 
        nn = n  
        if n > self._count:
            nn = self._count

        # Generate the return-list
        ls = []
        i = 0
        b_first=False # Did we pass _first?
        while (i < nn):
            if not (self._random_agent == not_this_agent):  # or (not_this_agent is None)
                ls.append(self._random_agent)
                i += 1

            if not (self._random_agent._next is None):
                self._random_agent = self._random_agent._next
            else:
                self._random_agent = self._first
                b_first=True

        # If we pass _first => new round => randomize 
        if b_first:
            self.randomize_agents()
        
        return ls


    def get_random_agent(self, not_this_agent=None, n=1):
        """A random child agent is returned

        Keyword Arguments:
            not_this_agent {Agent} -- An agent not to return. Will often be 'this'.  (default: {None})
            n {int} -- Number of agents to return. If the number of agents is less than n, all agents are returned.  (default: {1})

        Returns:
            Agent -- A random agent or a list of agents. Returns None if no children
        """
        if (not (not_this_agent is None)) and (not isinstance(not_this_agent, bool)):
            raise SystemExit('Error: Argument not_this_agent in get_random_agent should be None or bool.')

        if not isinstance(n, int):
            raise SystemExit('Error: Argument n in get_random_agent should be int.')
        
        ls = self.get_random_agents(not_this_agent=not_this_agent, n=n)

        if ls==None:
            return None

        if len(ls) == 1:
            return ls[0]
        else:
            return ls


    # Initialize iterator
    def __iter__(self):
        self._a_itt = self._first
        return self

    # Iterate iterator
    def __next__(self):
        if self._a_itt is not None:
            a = self._a_itt
            self._a_itt = self._a_itt._next
            return a
        else:    
            raise StopIteration

    def __eq__(self, other):
        return self._id==other

    def __ne__(self, other):
        return self._id!=other

    def __len__(self):
        if self._first==None:
            return 0
        else:
            return self._count

    def count(self):
        """Get the number of children

        Returns:
            int -- The number of children
        """
        return self._count
   
    def get_number_of_agents(self):
        """Get the number of children

        Returns:
            int -- The number of children
        """
        return self._count

    def number_of_agents(self):
        """Get the number of children

        Returns:
            int -- The number of children
        """
        return self._count

    def get_id(self):
        """Get the agents unique ID

        Returns:
            int -- Unique agent ID
        """
        return self._id

    @staticmethod
    def get_total_number_of_agents():
        """Get total number of agents in the current simulation

        Returns:
            int -- The total number of agents in the current simulation
        """
        return Agent._nAgents


# Poor man's loess. Fine and quick if many data points 
def local_mean(x,y, n=10):
    """Calculating local means. Poor man's loess. Fine and quick if many data points. 
    The algorithm works like this:
          1) x and y are sorted according to x, 
          2) the data is split in n equally sized parts, and
          3) means are calculated for both x and y in each part.     

    Arguments:
        x {list} -- The x data
        y {list} -- The y data

    Keyword Arguments:
        n {int} -- The number of parts (default: {10})

    Returns:
        {list, list} -- n mean values of x and y
    """

    xx, yy = (list(t) for t in zip(*sorted(zip(x, y)))) # sort x and y after x

    m = int(len(x)/n) # Number of data points in each group

    x_o, y_o = [], []
    x_sum, y_sum, v = 0, 0, 0
    j=1
    for i in range(len(x)):
        if v < m:
            x_sum += xx[i]
            y_sum += yy[i]
            v += 1
        else:
            x_o.append(x_sum/m)
            y_o.append(y_sum/m)
            x_sum, y_sum, v = 0, 0, 0
            j += 1

    return x_o, y_o 


