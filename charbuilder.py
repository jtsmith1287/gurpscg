'''
Created on Jul 31, 2013

@author: Justin & Theophilus
'''


import operator
import random

from stuff.utilities import utils
from stuff.tables import *
from stuff.headers import *
from stuff.parser import Parse
from traits.traits import *

parser = Parse()
parse = parser.parse

class CharacterBuilder:
  """Forms everything about the character."""

  def __init__ (self, form_data):
  
    self.misc = {"total_points": form_data["points"],
                 "spent_points": form_data["points"],
                 "build": None,
                 "age": random.randint(18, 64),
                 "gender": random.choice(["Male", "Female"]),
                 "TL": form_data["tl"]}
    self.basic_attributes = {"ST": 10, "DX": 10,   "IQ": 10,  "HT": 10,
                             "HP": 10, "Will": 10, "Per": 10, "FP": 10}
    self.secondary_attributes = {}
    self.wealth = {}
    self.appearance = {}
    self.encumbrance = {}
    self.skills = {"skills": [], 
                   "skill_limit": (self.misc["total_points"] + self.calcDisadvantageLimit(
                       form_data["points"], form_data["d_limit"])) * 0.24,
                   "categories": form_data["categories"]}
    self.advantages = {"advantages": [],
                       "adv_types": form_data["adv_types"]}
    self.disadvantages = {"disadvantages": [],
                          "disadvantage_points": 0,
                          "disadv_types": form_data["disadv_types"],
                          "disadvantage_limit": self.calcDisadvantageLimit(
        form_data["points"], form_data["d_limit"])}

    self.build()

  def formattedItems(self, item_list, header=None):
    """Formats a list of items into html.
    
    Args:
      item_list: a list of items.
    Returns:
      formatted_skills: a string of all items as html
    """
    new_item_list = []
    for item in item_list:
      formatted_item = []
      for item in item:
        formatted_item.append("<td> %s </td>" %(item))
      new_item_list.append("<tr> %s </tr>" %("".join(formatted_item)))

    table_tag = "<table border=\"5\">%s%s</table>"
    formatted_items = table_tag %(header, "".join(sorted(new_item_list)))
    return formatted_items

  def setAppearance(self):
    """Sets height, weight, build, and physical appearance."""
    height_options = utils.getColumnFromTable(HEIGHT_TABLE, "height")
    while True:
      self.misc["build"] = BUILD_TABLE[0][utils.randBiDistrib(BUILD_TABLE[0], 2)]
      build_options = utils.getColumnFromTable(BUILD_TABLE, self.misc["build"])
      if self.checkDisadvantageLimit(build_options[-1]):
        break

    while True:
      physical_appearance = APPEARANCE_TABLE[0][utils.randBiDistrib(APPEARANCE_TABLE[0], 5)]
      appearance_choice = utils.getColumnFromTable(APPEARANCE_TABLE, physical_appearance)
      if self.checkDisadvantageLimit(appearance_choice[-1]):
        break

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
    self.updateDisadvantagePoints(build_options[-1])
    self.updatePoints(build_options[-1])
    self.updateDisadvantagePoints(appearance_choice[-1])
    self.updatePoints(appearance_choice[-1])

  def setWealth(self):
    """Randomly selects starting wealth and status.

    Returns:
      wealth: a dictionary containing all wealth attributes for the character
    """

    wealth = {}
    while True:
      wealth_status = WEALTH_TABLE[0][utils.randWeight(WEALTH_TABLE[0])]
      starting_wealth = STARTING_WEALTH[self.misc["TL"]]
      wealth_details = utils.getColumnFromTable(WEALTH_TABLE, wealth_status)
      if self.checkDisadvantageLimit(wealth_details[-1]):
        break
    wealth["starting_cash"] = "{:,}".format(int(starting_wealth * wealth_details[1]))
    wealth["status"] = wealth_status
    wealth["status_description"] = wealth_details[0]
    self.wealth.update(wealth)
    self.updateDisadvantagePoints(wealth_details[-1])
    self.updatePoints(wealth_details[-1])

  def calculateMisc(self):
    """Sets basic speed, size, thrust, swing, basic move/lift and encumberance."""
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

  def updateSecondaryAttributes(self):
    """Updates HP, perception, will and fatigue based on stats."""
    self.basic_attributes["HP"] = self.basic_attributes["ST"]
    self.basic_attributes["Per"] = self.basic_attributes["IQ"]
    self.basic_attributes["Will"] = self.basic_attributes["IQ"]
    self.basic_attributes["FP"] = self.basic_attributes["HT"]

  def updateAttrPoints(self, stat, mod):
    """Determines if an attribute costs 10 or 20 points to raise and deducts the points.
    Args:
      stat: string of the attribute in question
      mod: how much the attribute is being raised
    """
    if stat in ["DX", "IQ"]:
      cost = mod * 20
    elif stat in ["ST", "HT"]:
      cost = mod * 10
    elif stat in ["Will", "Per"]:
      cost = mod * 5
    elif stat == "FP":      
      cost = mod * 3
    elif stat == "HP":
      cost = mod * 2

    self.updatePoints(cost)

  def updatePoints(self, points):
    """Subtracts the proposed amount from the available point total.
    Args:
      points: int of the amount of points to subtract from the available point total
    """
    self.misc["spent_points"] -= points; return True

  def getPrimaryAttribute(self):
    """Gets current highest attribute.

    Returns:
      max_attr: a string of random highest basic_attribute
    """
    
    primary_stats = ["ST", "DX", "IQ", "HT"]
    iter_list = (v for k,v in self.basic_attributes.items() if k in primary_stats)
    biggest = max(iter_list)
    max_attrs = []
    for stat,value in self.basic_attributes.items():
      if value >= biggest and stat in primary_stats:
        max_attrs.append(stat)
    max_attr = random.choice(max_attrs)

    return max_attr

  def updateDisadvantagePoints(self, points):
    """This updates the points spent on disadvantages.
    Args:
      points: int of point total change about to occur
    Note: This method is kept separate from updatePoints to leave room for 
          negative point changes that don't count toward disadvantage limit
    """
    if points < 0:
      self.disadvantages["disadvantage_points"] -= points
    
  def checkDisadvantageLimit(self, points):
    """Makes sure the proposed point change doesn't exceed the disadvantage limit.
    Args:
      points: int of proposed point value to be added to disadvantage points spent
    Returns:
      True or False: True if proposed point change will not exceed the disadvantage limit
    Note: the -5 leaves up to 5 points of wiggle room for overspending and to pick quirks
    """
    if (self.disadvantages["disadvantage_points"] - points) <= (
          self.disadvantages["disadvantage_limit"] - 5):
      return True
    else:
      return False

  def calcDisadvantageLimit(self, points, limit_key):
    """Determines and sets the disadvantage limit.
    Args:
      points: int of the point total
      limit_key: user specified limit to disadvantage points
    """
    if int(limit_key) == 0:
      d_limit = random.randint(0, int(points * 0.5))
    else:
      d_limit = int(limit_key)
    
    return d_limit    

  def cleanAds(self, ads):
    """Removes categories and TL from (dis)advantages.
    Args:
      ads: list of characters (dis)advantages
    """
    
    for advantage in ads:
      advantage.pop(-1)
      advantage.pop(-1)

  def auditSkillPrereqs(self):
    """Checks for skills that have unfulfilled prerequisites and removes them.
    Returns:
      True or False: based on whether the characters skills have all prerequisites met
    """
    for skill in self.skills["skills"]:
      if not self.checkPrereqs(skill):
        self.skills["skills"].remove(skill)
        return False
    return True

  def checkPrereqs(self, skill):
    """Checks if the prerequisites for a skill are met.
    Args:
      skill: the skill to check
    Returns:
      True or False: based on whether all prerequisites for the given skill are met
    """
    prereqs = skill[4]
    current_skills = [i[0] for i in self.skills["skills"]]
    current_advantages = [i[0] for i in self.advantages["advantages"]]

    for block in prereqs:

      if "or" in block:
        or_split = block.split(" or ")
        advantage_or_list = []
        for item in or_split:
          if "Advantage" in item:
            advantage_or_list.append(item.replace(" Advantage",""))
          elif item not in current_skills:
            return False
        if advantage_or_list and not any(
            i in current_advantages for i in advantage_or_list):
          return False

      elif "Advantage" in block:
        advantage = block.replace(" Advantage","")
        if advantage not in current_advantages:
          return False

      elif "+" in block:
        target_acquired = None
        items = block.split(" ")
        name, value = items[:-1], int(items[-1].replace("+", ""))
        for trait in self.skills["skills"]:
          if name in trait[0]:
            if trait[-2] >= value:
              target_acquired = True
        if not target_acquired:
          return False

      elif block not in current_skills:
        return False
    return True

  def updateSkillLevels(self):
    """Calculates and inserts the level of each skill or updates if it already exists."""
    for skill in self.skills["skills"]:
      if len(skill) == 8:
        skill.insert(-1, self.basic_attributes[skill[1]] + skill[-2])
      else: #the skill has been already been updated once before
        skill[-2] = self.basic_attributes[skill[1]] + skill[-3]

  def cleanSkills(self):
    """Removed unwanted syntax and makes skill look more purty.
    """
    for skill in self.skills["skills"]:
      skill[3] = self.misc["TL"]
      skill.pop(4)

  def chooseSkillCategories(self):
    """Chooses between 1 and 4 skill categories if not already chosen."""
    # The key == how many skill categories the character will have.
    skill_cats = self.skills["categories"]
    if not skill_cats:
      template = {1: "Focused",
                  2: "Specialized",
                  3: "Blended",
                  4: "Well Rounded"}
      for i in xrange(random.randint(1, len(template))):
        while True:
          cat = random.choice(list(SKILL_CATEGORIES))
          if cat not in skill_cats:
            skill_cats.append(cat)
            break
      # self.skills["focus"] = template[len(skill_cats)]
      self.skills["categories"] = skill_cats

  def getPossibleSkills(self):
    """Creates a list of likely skills based on characters selected categories and TL.
    Returns:
      possible_skills: a list of skills fitting the character's category and tech level
    """
    possible_skills = []
    for skill in SKILLS:
      if self.misc["TL"] >= skill[3][0] and self.misc["TL"] <= skill[3][1]:
        for cat in self.skills["categories"]:
          if cat in skill[-1] and skill not in possible_skills: # do we need this and here?
            # [-1]: references category of the skill
            possible_skills.append(skill)

    return possible_skills

  def getGoodCandidateSkills(self, possible_skills):
    """Generates a list of skills based on a given attribute.

    Args:
      possible_skills: list of the skills that match the characters categories and TL.
    Returns:
      good_candidates: list of skill from possible skill filtered by primary attribute
    """
    good_candidates = []
    p_attr = self.getPrimaryAttribute()
    for skill in possible_skills:
      if p_attr in skill[1] and skill not in good_candidates: # do we need this and here?
        # [1]: references attribute of skill
        good_candidates.append(skill)

    return good_candidates

  def setSkillLevel(self, skill):
    """Randomly sets the level of the skill.
    Args:
      skill: a list that is the skill to be leveled.
    Returns:
      skill: the skill with it's skill level appended.
    """
    skill_difficulty = skill[2]
    # We get the list of possible point costs
    point_table = utils.getColumnFromTable(SKILL_COST_TABLE, "PS")
    # Then we'll get a weighted random point cost from that list
    points_to_spend = point_table[utils.randBiDistrib(point_table, 1)]
    while points_to_spend > int(self.misc["spent_points"]) + 5:
      points_to_spend = point_table[utils.randBiDistrib(point_table, 1)]
    # We'll need the column for where we're going to get the relative skill level
    # based on the already chosen point cost
    table_index = SKILL_COST_TABLE[0].index(skill_difficulty)
    # This is where we get the row for all possible difficulties associated with
    # that point cost
    skill_levels = utils.getRowFromTable(SKILL_COST_TABLE, points_to_spend)
    # And now we actually get our skill level and we'll replace the skill
    # categories with the relative level, and then extend the skill to show the
    # actual level (which is the base attribute + the relative level
    relative_level = skill_levels[table_index]
    skill[-1] = relative_level
    skill.append(points_to_spend)
    self.updatePoints(points_to_spend)

    return skill

  def pickSkill(self):
    """Picks a skill at random from skill_lists.
    Returns:
      skill: a list that is the chosen skill
    """
    skill = []
    probable_skills = self.getPossibleSkills()
    good_candidates = self.getGoodCandidateSkills(probable_skills)
    chance = random.randint(1, 10)
    while not skill:
      if good_candidates and chance > 2:
        skill_list = good_candidates
      elif probable_skills and chance < 2:
        skill_list = probable_skills
      else:
        return
      skill_choice = random.choice(skill_list)[:]
      if skill_choice[0] in [ass[0] for ass in self.skills["skills"]]:
        skill_list.remove(skill_choice)
      else:
        skill = skill_choice
    # If this is the first skill then we want to increase the primary attr
    if not self.skills["skills"]:
      attr = skill[1]
      p_attrs =  ["ST", "DX", "IQ"]
      if attr not in p_attrs:
        attr = random.choice(p_attrs)
      self.basic_attributes[attr] += 2
      self.updateAttrPoints(attr, 2)
    # Set the level of a copy of the skill and return the copy
    skill = self.setSkillLevel(skill[:])

    return skill

  def increaseRandomAttribute(self):
    """Picks an attribute to increase by one, weighted towards the highest attribute."""
    attrs = {}
    # Find most common stat shared by skills
    for skill in self.skills["skills"]:
      try:
        attrs[skill[1]] += 1
      except KeyError:
        attrs[skill[1]] = 1

    if (int(self.misc["spent_points"]) + 5) < 20:
      choice = random.choice(["HT", "ST"])
      self.updateAttrPoints(choice, 1)
      self.basic_attributes[choice] += 1
    else:
      high_attr = max(attrs.iteritems(), key=operator.itemgetter(1))[0]
      chance = random.random()
      if chance < 0.4001:
        self.updateAttrPoints(high_attr, 1)
        self.basic_attributes[high_attr] += 1
      else:
        attr_choices = ["ST", "HT", "IQ", "DX"]
        if high_attr in attr_choices:
          attr_choices.remove(high_attr)
        highest_attr = random.choice(attr_choices)
        self.updateAttrPoints(highest_attr, 1)
        self.basic_attributes[highest_attr] += 1

  def decreaseRandomAttribute(self):
    """Picks one of the lowest attributes and reduces it by 1."""
    primary_stats = ["ST", "DX", "IQ", "HT"]
    stats = {}
    for k,v in self.basic_attributes.items():
      if k in primary_stats:
        stats[k] = v
    low = [k for k, v in stats.items() if not any(y < v for y in stats.values())]
    if len(low) == 1:
      stats.pop(low[0])
      low.append(min(stats, key=stats.get))
      choice = random.choice(low)
    else:
      choice = random.choice(low)

    if self.basic_attributes[choice] > 7: # <--- Minimum possible stat
      self.updateAttrPoints(choice, -1)
      self.basic_attributes[choice] -= 1

  def pickAdvantage(self, advantages_list):
    """Picks an advantage! Yaaaayy!
    Args:
      advantages_list: a list of advantages filtered by choice for X/Sup
    """
    pa = self.getPrimaryAttribute()
    if pa in ["HT", "ST", "DX"]:
      attr_type = "P"
    else: 
      attr_type = random.choice(["M", "Soc"])
    
    pa_based_list = [i for i in advantages_list if i[1] == attr_type and i[0] not in [
        name[0] for name in self.advantages["advantages"]]]
    cat_list = [i for i in advantages_list if any(
                    cat in self.skills["categories"] for cat in i[-1]) and (
                        i[0] not in [name[0] for name in self.advantages["advantages"]])]
    ideal_list = [i for i in pa_based_list if i in cat_list]

    while True:
      if random.random() > .05:
        if ideal_list:
          chosen_advantage = random.choice(ideal_list)[:]
        else:
          chosen_advantage = random.choice(pa_based_list)[:]
      else:
        while True:
          chosen_advantage = random.choice(advantages_list)[:]
          if chosen_advantage[0] not in [i[0] for i in self.advantages["advantages"]]:
            break
      points = parse(chosen_advantage[3])
      if points < int(self.misc["spent_points"]) + 5:
        break

    self.updatePoints(points)
    chosen_advantage[3] = points
    self.advantages["advantages"].append(chosen_advantage)

  def pickDisadvantage(self, disadvantages_list):
    """Picks a disadvantage!.. awh shucks.
    Args:
      disadvantages_list: a list of disadvantages filtered by choice for X/Sup
    """
    pa = self.getPrimaryAttribute()
    if pa in ["HT", "ST", "DX"]:
      attr_type = random.choice(["M", "Soc"])
    else: 
      attr_type = "P"
    point_check = True
    
    # If we're about maxed on disadvantages and spent points, pick quirks instead
    if self.misc["spent_points"] < 0:
      points_left = (self.disadvantages["disadvantage_limit"]) - (
          self.disadvantages["disadvantage_points"])
      if points_left <= 5:
        for unused_point in range(points_left):
          self.updatePoints(-1)
          self.disadvantages["disadvantages"].append(
              ["Quirk", "M/P/Soc", "-", -1, "162"])
          if self.misc["spent_points"] == 0:
            return
        
    while True:
      if random.random() > .05:
        pa_based_list = [i for i in disadvantages_list if i[1] == attr_type and i[0] not in [
            name[0] for name in self.disadvantages["disadvantages"]]]
        chosen_disadvantage = random.choice(pa_based_list)[:]
      else:
        while True:
          chosen_disadvantage = random.choice(disadvantages_list)[:]
          if chosen_disadvantage[0] not in [i[0] for i in self.disadvantages["disadvantages"]]:
            break
      
      points = parse(chosen_disadvantage[3])
      if self.checkDisadvantageLimit(points):
        break

    self.updateDisadvantagePoints(points)
    self.updatePoints(points)
    chosen_disadvantage[3] = points
    self.disadvantages["disadvantages"].append(chosen_disadvantage)

  def runCharacterBuildLoop(self):
    """Runs the loop that picks skills/(dis)advantages and in/decreases attributes."""
    advantage_list = [
        i for i in ADVANTAGES_LIST[:] if i[2] in self.advantages["adv_types"]]
    disadvantages_list = [
        i for i in DISADVANTAGES_LIST[:] if i[2] in self.disadvantages["disadv_types"]]

    while self.misc["spent_points"] > 0:
      spend_limit = int(self.misc["spent_points"]) + 5
      choice = random.randint(1, 100)
      skill_points = sum([n[-1] for n in self.skills["skills"]])
      # Add a skill
      if choice < 85 and self.skills["skill_limit"] > skill_points:
        raw_skill = self.pickSkill()
        if not raw_skill:
          continue
        self.skills["skills"].append(raw_skill)
      # Increase a stat
      elif (choice > 85) and (choice < 92) and spend_limit > 10:
        if not self.skills["skills"]:
          continue
        self.increaseRandomAttribute()
      # Add an advantage
      elif (choice > 91) and (choice < 95):
        self.pickAdvantage(advantage_list)
      # Decrease a stat
      elif (choice > 94) and (choice < 98):
        self.decreaseRandomAttribute()
      # Add a disadvantage
      elif (choice > 97) and self.checkDisadvantageLimit(-5):
        self.pickDisadvantage(disadvantages_list)
      # Add a disadvantage when out of points
      while self.misc["spent_points"] < 0:
        self.pickDisadvantage(disadvantages_list)    

  def build(self):
    """Assembles all of the above madness into a character."""
    # Sets height, weight, appearance and physical build
    self.setAppearance()
    # Sets starting wealth attributes
    self.setWealth()
    # Configures all other attributes of the character
    self.chooseSkillCategories()
    while True:
      self.runCharacterBuildLoop()
      self.updateSecondaryAttributes()
      self.updateSkillLevels()
      if self.auditSkillPrereqs():
        break
    self.cleanAds(self.advantages["advantages"])
    self.cleanAds(self.disadvantages["disadvantages"])
    self.cleanSkills()
    self.skills["skills"] = self.formattedItems(self.skills["skills"], SKILL_HEADER)
    self.advantages["advantages"] = self.formattedItems(
        self.advantages["advantages"], ADVANTAGE_HEADER)
    self.disadvantages["disadvantages"] = self.formattedItems(
        self.disadvantages["disadvantages"], DISADVANTAGE_HEADER)
    self.calculateMisc()

if __name__ == "__main__":

  def mergeDicts(master_dict):
    new_dict = []
    for dictionary in master_dict.keys():
      if not dictionary:
        continue
      new_dict.extend(master_dict[dictionary].items())
    return dict(new_dict)

  fd = {"points": 150,
      "tl": 11,
      "adv_types": ["-", "X", "Sup"]
      }
  nc = CharacterBuilder(fd)  

