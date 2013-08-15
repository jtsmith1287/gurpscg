'''
Created on Jul 24, 2013

@author: Justin
'''
import random

class Utilities:
    
  def getColumnFromTable (self, table, header):

    return [i[table[0].index(header)] for i in table[1:]]

  def randWeight(self, array, dice=3):
    """Returns a random index simulating a dice roll."""

    return int(sum([random.randint(0, len(array)-1) for i in xrange(dice)])/dice)
  
  def randBiDistrib(self, array, median):
    """Returns a random index using binomial distribution."""
    l = len(array)
    return sum([1 if random.random() < (float(median)/l) else 0 for i in xrange(l)])-1

utils = Utilities()