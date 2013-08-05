'''
Created on Jul 24, 2013

@author: Justin
'''
import random

class Utilities:
    
  def getColumnFromTable (self, table, header):

    return [i[table[0].index(header)] for i in table[1:]]

  def randWeight(self, arg, dice=3):

    return int(sum([random.randint(0, len(arg)-1) for i in xrange(dice)])/dice)