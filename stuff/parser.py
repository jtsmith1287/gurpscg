'''
Created on Oct 17, 2013

@author: Justin
'''
import random
import re


def getdigit(string):
  "returns the literal numeric value from the passed string"
  
  try:
    num = int(string)
  except ValueError:
    num = None
  
  return num

def cleaner(to_clean):
  for i in to_clean[:]:
    if i == "" or i == " ":
      to_clean.remove(i)

class Parse:

  def parse (self, text):
    """
    """
    if "/level" in text:
      base = 0
      if "---" in text:
        limit = int(text.split("---")[-1])
      else: limit = 5
      levels = random.randint(1, limit)
      options = re.split("/level| or |,|---\d?", text)
      if "+" in text:
        base, multiplier = map(int, options[0].split(" + "))
        options = [multiplier]
      cleaner(options)
      picked = (int(random.choice(options)) * levels) + base
    else:
      split_pattern = " or | to |Variable===|,"
      options = re.split(split_pattern, text)
      cleaner(options)
      picked = random.choice(options)
  
    point_value = getdigit(picked)
    return point_value