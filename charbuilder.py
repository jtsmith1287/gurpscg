'''
Created on Jul 31, 2013

@author: Justin
 & Theophilus
'''

from tables import *
import random
import utilities


utils = utilities.Utilities()

BUILD_OPTIONS = ["Skinny", "Average", "Average", "Overweight", "Fat", "Very Fat"]

class CharacterBuilder:
  """Forms everything about the character
"""

  def __init__ (self, points):
  
    self.misc = {"points": points,
                 "build":  BUILD_OPTIONS[utils.randWeight(BUILD_OPTIONS)],
                 "age": random.randint(18, 64),
                 "gender": random.choice(["Male", "Female"])}
    self.basic_attributes = {"ST": 10,
                             "DX": 10,
                             "IQ": 10,
                             "HT": 10,
                             "HP": 10,
                             "Will": 10,
                             "Per": 10,
                             "FP": 10}
    self.secondary_attributes = {}
    self.wealth = {"TL": random.randint(0, 12)}
    self.appearance = {}
    self.encumbrance = {}
    self.languages = {}
    self.skills = {}
    self.advantages = {}
    self.disadvantages = {"disadvantage_limit": random.randint(0, points/2)}

    self.build()
  
  def updatePoints(self, points):

    self.misc["points"] -= points
    if self.misc["points"] < 0:
      self.misc["points"] += points
      return False
    else:
      return "balls" # Equivalent to True ... why not, right?

  def setAppearance(self):
      
    height_options = utils.getColumnFromTable(BUILD_TABLE, "height")
    build_options = utils.getColumnFromTable(BUILD_TABLE, self.misc["build"])
    physical_appearance = APPEARANCE_TABLE[0][utils.randWeight(APPEARANCE_TABLE[0])]
    appearance_choice = utils.getColumnFromTable(APPEARANCE_TABLE, physical_appearance)
    st = self.basic_attributes["ST"]
    if st < 6:
      st = 6
    elif st > 14:
      st = 14
    table_index = st - 6 # 6 is the lowest value in the table, which gives us 0
    # Set weight
    range = build_options[table_index]
    self.appearance["weight"] = str(random.randint(range[0], range[1])) + "lbs"
    # Set height
    ranges = (map(int, str(height_options[table_index][0]).split(".")),
              map(int, str(height_options[table_index][1]).split(".")))
    range_in_inches = (ranges[0][0] * 12 + ranges[0][1],
                       ranges[1][0] * 12 + ranges[1][1])
    height = divmod(random.randint(range_in_inches[0], range_in_inches[1]), 12)
    self.appearance["height"] = "%s ft %s inches" %(height[0], height[1])
    # Set physical appearance
    self.appearance["physical_appearance"] = "%s<br>%s" % (physical_appearance, appearance_choice[0])
    # Set points
    self.updatePoints(build_options[-1])
    self.updatePoints(appearance_choice[-1])

  def setWealth(self):
    wealth_type = WEALTH_TABLE[0][utils.randWeight(WEALTH_TABLE[0])]
    starting_wealth = STARTING_WEALTH[self.wealth["TL"]]
    wealth_details = utils.getColumnFromTable(WEALTH_TABLE, wealth_type)
    self.wealth["Starting Cash"] = starting_wealth * wealth_details[1]
    self.wealth["status"] = wealth_details[0]
    self.updatePoints(wealth_details[-1])

  def build(self):
    self.setAppearance()
    self.setWealth()
    










                          
                                                            