'''
Created on Jul 31, 2013

@author: Justin
 & Theophilus
'''

from tables import *
import random
from utilities import utils


class CharacterBuilder:
  """Forms everything about the character."""

  def __init__ (self, points):
  
    self.misc = {"total_points": points,
                 "spent_points": points,
                 "build":  BUILD_TABLE[0][utils.randBiDistrib(BUILD_TABLE[0], 2)],
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
    self.wealth = {"TL": 9}
    self.appearance = {}
    self.encumbrance = {}
    self.skills = {}
    self.advantages = {}
    self.disadvantages = {"disadvantage_limit": random.randint(0, points/2)}

    self.build()
  
  def updatePoints(self, points):

    if (self.misc["spent_points"] - points) > -1:
      self.misc["spent_points"] -= points; return True

  def setAppearance(self):
      
    height_options = utils.getColumnFromTable(HEIGHT_TABLE, "height")
    build_options = utils.getColumnFromTable(BUILD_TABLE, self.misc["build"])
    physical_appearance = APPEARANCE_TABLE[0][utils.randBiDistrib(APPEARANCE_TABLE[0], 5)]
    appearance_choice = utils.getColumnFromTable(APPEARANCE_TABLE, physical_appearance)

    st = self.basic_attributes["ST"]
    if st < 6:
      st = 6
    elif st > 14:
      st = 14
    table_index = st - 6 # 6 is the lowest value in the table, which gives us 0

    # Set weight
    w_range = build_options[table_index]
    self.appearance["weight"] = str(random.randint(w_range[0], w_range[1])) + "lbs"

    # Set height
    ranges = (map(int, str(height_options[table_index][0]).split(".")),
              map(int, str(height_options[table_index][1]).split(".")))
    range_in_inches = (ranges[0][0] * 12 + ranges[0][1],
                       ranges[1][0] * 12 + ranges[1][1])
    height = divmod(random.randint(range_in_inches[0], range_in_inches[1]), 12)
    self.appearance["height"] = "%s ft %s inches" %(height[0], height[1])

    # Set physical appearance
    self.appearance["physical_appearance"] = "%s<br>%s" % (
        physical_appearance, appearance_choice[0])

    # Set points
    self.updatePoints(build_options[-1])
    self.updatePoints(appearance_choice[-1])

  def setWealth(self):

    wealth_status = WEALTH_TABLE[0][utils.randWeight(WEALTH_TABLE[0])]
    starting_wealth = STARTING_WEALTH[self.wealth["TL"]]
    wealth_details = utils.getColumnFromTable(WEALTH_TABLE, wealth_status)

    self.wealth["starting_cash"] = "{:,}".format(int(starting_wealth * wealth_details[1]))
    self.wealth["status"] = wealth_status
    self.wealth["status_description"] = wealth_details[0]
    self.updatePoints(wealth_details[-1])

  def tmpRandomStats(self):

    skip = {"Per":"IQ", "HP":"ST", "Will":"IQ", "FP":"HT"}

    for stat in self.basic_attributes:
      if stat in skip.keys(): continue
      mod_options = [i - 4 for i in xrange(9)] #generate list from -4 to 4
      mod = mod_options[utils.randWeight(mod_options, 4)]
      self.basic_attributes[stat] += mod
      if stat in ["DX","IQ"]:
        self.updatePoints(mod * 20)
      elif stat in ["ST","HT"]:
        self.updatePoints(mod * 10)
    
    for other in skip:
      mod_options = [i - 3 for i in xrange(7)] #generate list from -3 to 3
      mod = mod_options[utils.randBiDistrib(mod_options, 5)]
      self.basic_attributes[other] = self.basic_attributes[skip[other]] + mod
      if other in ["Will","Per"]:
        self.updatePoints(mod * 5)
      elif other == "FP":      
        self.updatePoints(mod * 3)
      else:
        self.updatePoints(mod * 2)

  def calculateMisc(self):

    ST = self.basic_attributes['ST']
    DX = self.basic_attributes['DX']
    HT = self.basic_attributes['HT']
    self.secondary_attributes['basic_speed'] = (HT+DX)/4
    self.secondary_attributes['SM'] = 0
    self.secondary_attributes['thrust'] = DAMAGE_TABLE[ST+1][0]
    self.secondary_attributes['swing'] = DAMAGE_TABLE[ST+1][1]
    self.secondary_attributes['basic_move'] = int(self.secondary_attributes['basic_speed'])
    self.secondary_attributes['basic_lift'] = (ST*ST)/5
    self.secondary_attributes['none'] = 2 * ((ST*ST)/5)
    self.secondary_attributes['light'] = 4 * ((ST*ST)/5)
    self.secondary_attributes['medium'] = 6 * ((ST*ST)/5)
    self.secondary_attributes['heavy'] = 12 * ((ST*ST)/5)
    self.secondary_attributes['extra_heavy'] = 20 * ((ST*ST)/5)


  def build(self):

    self.setAppearance()
    self.setWealth()
    self.tmpRandomStats()
    self.calculateMisc()

    self.advantages["a_notice"] = "Feature coming soon!"
    self.disadvantages["d_notice"] = "Feature coming soon!"
    self.skills["s_notice"] = "Feature coming soon!"






                          
                                                            