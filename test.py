'''
Created on Aug 5, 2013

@author: Justin
'''
import random
if __name__ == "__main__":
  y = 9.0
  print sum([1 if random.random() < (6.0/9.0) else 0 for i in xrange(int(y))])