import random

"""
The SimRandom class is a wrapper around random, providing only the 
randint(bound) method -- returns a random number between 0 and bound-1. The reason
for this class is that SimRandom is deterministic, it gives the same numbers in any simulation run.
  
So, for testing, the "random" choice of Orders and Inventory will be predictable,
which is nice for testing and debugging purposes.
"""

class SimRandom:

    # Constructior just creates random witha seed value, so that every new
    # SimRandom object will have the same sequence of pseudo-ranom numbers
    def __init__(self):
        random.seed(24) # Give inital seed for determinism

    def randint(self, bound):
        return random.randint(0, bound - 1)


#a = SimRandom()

#print(a.randint(5))






