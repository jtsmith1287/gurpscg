'''
Created on Aug 5, 2013

@author: Justin
'''
import random
if __name__ == "__main__":

  stuff = ["birds", "canine", "monkey", "really really stupid"]
  
  search_term = raw_input(": ")
  search_result = None

  for word in stuff:
    match = True
    for idx in xrange(len(search_term)):
      if word[idx] != search_term[idx]:
        match = False
    if match:
      search_result = word

print search_result