'''
Created on Jul 24, 2013

@author: Justin
'''
import random
import functools

class Memoize(object):
  """Cache the result of a call and return that if it's being passed the same args"""
  
  def __init__(self, func): 
    self.func = func 
    self.memoized = {} 
    self.method_cache = {} 
  def __call__(self, *args): 
    return self.cache_get(self.memoized, args, lambda: self.func(*args)) 
  def __get__(self, obj, objtype): 
    return self.cache_get(self.method_cache, obj, lambda: self.__class__(
        functools.partial(self.func, obj))) 
  def cache_get(self, cache, key, func): 
    try: 
      return cache[key] 
    except KeyError: 
      cache[key] = func() 
      return cache[key]

class Utilities:
    
  def getColumnFromTable (self, table, header):

    return [i[table[0].index(header)] for i in table[1:]]
  
  def getRowFromTable(self, table, row_name):
    
    for row in table[1:]:
      if row[0] == row_name:
        return row

  def randWeight(self, array, dice=3, min=0):
    """Returns a random index simulating a dice roll."""

    return int(sum([random.randint(min, len(array)-1) for unused in xrange(dice)])/dice)
  
  def randBiDistrib(self, array, median):
    """Returns a random index using binomial distribution."""
    l = len(array)
    return sum([1 if random.random() < (float(median)/l) else 0 for unused in xrange(l-1)])
  
utils = Utilities()