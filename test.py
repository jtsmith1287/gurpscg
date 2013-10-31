'''
Created on Aug 5, 2013

@author: Justin
'''
import random
if __name__ == "__main__":

  stuff = ["birds", "canine", "monkey", "really really stupid"]
  
  search_term = raw_input(": ")

  for word in stuff:
    match = False
    for idx in xrange(len(search_term)):
      if word[idx] !=