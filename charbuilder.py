'''
Created on Jul 31, 2013

@author: Justin & Theophilus
'''


import operator
import random
import logging
from stuff.utilities import Memoize, utils
from stuff.tables import *
from stuff.headers import *
from stuff.parser import Parse
from traits.traits import *

parser = Parse()
parse = parser.parse


def Print(*args):
  logging.info(args) 

class CharacterBuilder:
  """Forms everything about the character."""

  def __init__ (self, form_data):
  
    self.misc = {"total_points": form_data["points"],
                 "spent_points": form_data["points"],
                 "build": None,
                 "age": utils.randWeight(range(18, 65), 2, 18),
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
                       "adv_types": form_data["adv_types"],
                       "talents" : {}}
    self.disadvantages = {"disadvantages": [],
                          "disadvantage_points": 0,
                          "disadv_types": form_data["disadv_types"],
                          "disadvantage_limit": self.calcDisadvantageLimit(
        form_data["points"], form_data["d_limit"])}
    self.spells = {"spells": [],
                   "spell_colleges": form_data["spell_colleges"]}
    self.primary_attributes = {"pa":form_data["pa"],
                               "sa":form_data["sa"],
                               "ta":form_data["ta"]}
    self.fool_me = {"once" : [], "twice" : [], "speller" : {}}
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
  
  @Memoize
  def getBaseStats(self):
    """Gets the base stats before starting to help determine disadvantage points.
    Note: memoized to prevent recalculation after things get rolling and to avoid being
          stored in init since that gets used to populate the html stuff."""
    base_stats = {} # all 10 for now, though eventually racial templates will happen
    for stat in [k for k,v in self.basic_attributes.items() if k in ["ST", "DX", "IQ", "HT"]]:
      base_stats[stat[:]] = v
    return base_stats

  @Memoize
  def getChoices(self):
    """Anything the user specified that might be needed that gets overwritten later."""
    the_stuff = {}
    for k,v in self.primary_attributes.items():
      the_stuff[k] = v
    # Potentially more things here later
    return the_stuff

  def setAppearance(self):
    """Sets height, weight, build, and physical appearance."""
    height_options = utils.getColumnFromTable(HEIGHT_TABLE, "height")
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 82")
      self.misc["build"] = BUILD_TABLE[0][utils.randBiDistrib(BUILD_TABLE[0], 2)]
      build_options = utils.getColumnFromTable(BUILD_TABLE, self.misc["build"])
      if self.checkDisadvantageLimit(build_options[-1]):
        break
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 90")
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
    self.updatePoints(build_options[-1])
    self.updatePoints(appearance_choice[-1])

  def setWealth(self):
    """Randomly selects starting wealth and status.

    Returns:
      wealth: a dictionary containing all wealth attributes for the character
    """

    wealth = {}
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 146")
      wealth_status = WEALTH_TABLE[0][utils.randWeight(WEALTH_TABLE[0])]
      starting_wealth = STARTING_WEALTH[self.misc["TL"]]
      wealth_details = utils.getColumnFromTable(WEALTH_TABLE, wealth_status)
      if self.checkDisadvantageLimit(wealth_details[-1]):
        break
    wealth["starting_cash"] = "{:,}".format(int(starting_wealth * wealth_details[1]))
    wealth["status"] = wealth_status
    wealth["status_description"] = wealth_details[0]
    self.wealth.update(wealth)
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

  def updateAttrPoints(self, stat, mod, d_check=False):
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

    self.updatePoints(cost, d_check)

  def updatePoints(self, points, d_check=False):
    """Subtracts the proposed amount from the available point total.
    Args:
      points: int of the amount of points to subtract from the available point total
    """
    self.misc["spent_points"] -= points
    if points < 0 and not d_check:
      self.disadvantages["disadvantage_points"] -= points
    elif points > 0 and d_check:
      self.disadvantages["disadvantage_points"] -= points
      
  def determinePrimaryAttribute(self, proposed):
    """
    """
    p_attrs =  ["ST", "DX", "IQ"]

    # Nothing specified so pick primary and possibly a secondary at random
    if not any (i for i in self.primary_attributes.values()):
      if proposed not in p_attrs:
        proposed = random.choice(p_attrs)
      self.primary_attributes["pa"] = proposed
      p_attrs.append("HT")
      chance = random.randint(1, 2)
      if chance == 1:
        self.primary_attributes["sa"] = random.choice([
            i for i in p_attrs if proposed not in i])
        self.basic_attributes[self.primary_attributes["pa"]] += 1
        self.updateAttrPoints(self.primary_attributes["pa"], 1)
        self.basic_attributes[self.primary_attributes["sa"]] += 1
        self.updateAttrPoints(self.primary_attributes["sa"], 1)
      else:
        self.basic_attributes[self.primary_attributes["pa"]] += 2
        self.updateAttrPoints(self.primary_attributes["pa"], 2)
    # Just primary attribute was selected
    elif not self.primary_attributes["sa"] and not self.primary_attributes["ta"]:
      self.basic_attributes[self.primary_attributes["pa"]] += 2
      self.updateAttrPoints(self.primary_attributes["pa"], 2)
    # Secondary or Tertiary were selected
    else:
      if not self.primary_attributes["pa"]:
        if proposed not in p_attrs:
          proposed = random.choice(p_attrs)
        self.primary_attributes["pa"] = proposed
      self.basic_attributes[self.primary_attributes["pa"]] += 1
      self.updateAttrPoints(self.primary_attributes["pa"], 1)
      if self.primary_attributes["ta"]:
        self.basic_attributes[self.primary_attributes["ta"]] += 1
        self.updateAttrPoints(self.primary_attributes["ta"], 1)
      if self.primary_attributes["sa"]:
        self.basic_attributes[self.primary_attributes["sa"]] += 1
        self.updateAttrPoints(self.primary_attributes["sa"], 1)

  def checkDisadvantageLimit(self, points):
    """Makes sure the proposed point change doesn't exceed the disadvantage limit.
    Args:
      points: int of proposed point value to be added to disadvantage points spent
    Returns:
      True or False: True if proposed point change will not exceed the disadvantage limit
    Note: the -5 leaves up to 5 points of wiggle room for overspending and to pick quirks
    """
    if (self.disadvantages["disadvantage_points"] - points) <= (
          self.disadvantages["disadvantage_limit"] - 4):
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
      d_limit = random.randint(int(points * 0.1), int(points * 0.5))
    else:
      d_limit = int(limit_key)
    
    return d_limit

  def cleanAds(self, ads):
    """Removes categories and TL from (dis)advantages.
    Args:
      ads: list of characters (dis)advantages
    """
    
    for advantage in ads:
      if len(advantage) > 5:
        advantage.pop(-1)
        advantage.pop(-1)

  def auditSkillPrereqs(self):
    """Checks for skills that have unfulfilled prerequisites and removes them.
    Returns:
      True or False: based on whether the characters skills have all prerequisites met
    """
    check = True
    for skill in self.skills["skills"]:
      if not self.checkPrereqs(skill):
        if skill[0] in self.fool_me["once"]: # Prevents recursion
          self.fool_me["twice"].append(skill[0])
          self.fool_me["once"].remove(skill[0])
        else:
          self.fool_me["once"].append(skill[0])
        check = False
        Print("this skill failed prerequisites", skill[0])
        self.updatePoints(0-skill[-1], True)
        self.skills["skills"].remove(skill)
        for dis in self.disadvantages["disadvantages"]:
          if "Quirk" in dis[0]:
            self.disadvantages["disadvantages"].remove(dis)
            self.updatePoints(1, True)
    self.pickQuirks()
    if check:
      return True
    else:
      return False

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
        if advantage_or_list and not [i in advantage_or_list for i in current_advantages]:
          Print(advantage_or_list, current_advantages)
          return False

      elif "Advantage" in block:
        advantage = block.replace(" Advantage","")
        if advantage not in current_advantages:
          
          return False

      elif "+" in block:
        target_acquired = None
        items = block.split(" ")
        name, value = ' '.join(items[:-1]), int(items[-1].replace("+", ""))
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
    
    if self.spells["spells"]:
      for i in [x for x in self.advantages["advantages"] if "Magery" in x[0]]:
        magery_level = (int(i[3]) -5)/10
      for spell in self.spells["spells"]:
        if len(spell) == 11:
          spell.insert(-1, self.basic_attributes["IQ"]+spell[-2]+magery_level)
        else:
          spell[-2] = self.basic_attributes["IQ"]+spell[-3]+magery_level

  def cleanSkills(self):
    """Removed unwanted syntax and makes skill look more purty.
    """
    for skill in self.skills["skills"]:
      skill[3] = self.misc["TL"]
      skill.pop(4)

  def updatePsiTalents(self):
    """
    """
    if self.advantages["talents"]:
      for talent, value in self.advantages["talents"].items():
        points = value * 5
        name = "%s talent (%s)" % (talent, value)
        self.advantages["advantages"].append([name, "-", "Sup", points, "256/257"])

  def chooseSkillCategories(self):
    """Chooses between 1 and 4 skill categories if not already chosen."""
    # The key == how many skill categories the character will have.
    skill_cats = self.skills["categories"]
    unsatisfactory = ["Alien", "Cyborg"] # cats that don't have associated skills
    holding = []
    for mrowl in unsatisfactory:
      if mrowl in skill_cats:
        holding.append(mrowl)
        skill_cats.remove(mrowl)

    if not skill_cats:
      template = {2: "Focused",
                  3: "Specialized",
                  4: "Blended",
                  5: "Well Rounded"}
      for unused in xrange(random.randint(2, len(template))):
        cat = random.choice([i for i in SKILL_CATEGORIES if i not in skill_cats])
        skill_cats.append(cat)
      # self.skills["focus"] = template[len(skill_cats)]
    if holding:
      for meow in holding:
        skill_cats.append(meow)
    self.skills["categories"] = skill_cats

  def generateMustHaveLists(self, items):
    """Generates a list items that must be in the character per category choices.
    Args:
      items: A table of items to parse for things that must be in the character
    Returns:
      must_haves: a list of the items that just must be had
    """
    must_haves = []
    for item in items:
      meow = [cat for cat in item[-1] if "---" in cat]
      if meow:
        if cat.strip("---") in self.skills["categories"]:
          must_haves.append(item[:])

    return must_haves

  def getMustHaves(self):
    """Hunts down any skills or advantages required for categories checked.
    Returns:
      must_have_skills: list of skills the character must have based on category choices
      must_have_advantages: the poop smith's job is obvious
    """
    must_have_skills = self.generateMustHaveLists(SKILLS)
    must_have_advantages = self.generateMustHaveLists(ADVANTAGES_LIST)

    # Acquire all must-have skills
    if must_have_skills:
      for skill in must_have_skills:
        raw_skill = self.pickSkill(skill)
        self.skills["skills"].append(raw_skill)

    # Poop smith
    if must_have_advantages:
      for advantage in must_have_advantages:
        points = parse(advantage[3])
        self.updatePoints(points)
        advantage[3] = points
        self.advantages["advantages"].append(advantage)

  def getPossibleSkills(self):
    """Creates a list of likely skills based on characters selected categories and TL.
    Returns:
      possible_skills: a list of skills fitting the character's category and tech level
    """
    possible_skills = []
    for skill in SKILLS:
      if self.misc["TL"] >= skill[3][0] and self.misc["TL"] <= skill[3][1]:
        for cat in self.skills["categories"]:
          if cat in skill[-1] and skill[0] not in self.fool_me["twice"]:
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
    if not self.primary_attributes["pa"]:
      p_attr = random.choice(["ST", "DX", "IQ"])
    else:
      p_attr = self.primary_attributes["pa"]
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
    counter = 0
    while counter < 1000 and points_to_spend > int(self.misc["spent_points"]) + 3:
      counter +=1
      if counter > 998:Print("out of control while loop line 490")
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

  def pickSkill(self, skill=[]):
    """Picks a skill at random from skill_lists.
    Args:
      skill=[]: a list that is a skill that must be picked and bypasses some logic
    Returns:
      skill: a list that is the chosen skill
    """
    probable_skills = self.getPossibleSkills()
    good_candidates = self.getGoodCandidateSkills(probable_skills)        
    
    chance = random.randint(1, 10)
    counter = 0
    while not skill and counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 521")
      if good_candidates and chance > 2:
        skill_list = good_candidates
      elif probable_skills and chance < 3:
        skill_list = probable_skills
      else:
        return
      skill_choice = random.choice(skill_list)
      if skill_choice[0] in [ass[0] for ass in self.skills["skills"]]:
        skill_list.remove(skill_choice)
      else:
        skill = skill_choice
    # Set the level of a copy of the skill
    skill = self.setSkillLevel(skill[:])
    # If this is the first skill then we want to increase the primary attr
    if not self.skills["skills"]:
      self.determinePrimaryAttribute(skill[1])

    return skill

  def increaseRandomAttribute(self):
    """Picks an attribute to increase by one, weighted to the common skill attribute."""
    secondary = self.primary_attributes["sa"]
    tertiary = self.primary_attributes["ta"]
    attrs = {}
    primary_attributes = ["ST", "HT", "IQ", "DX"]
    choice = None
    chance = random.random()
    if (int(self.misc["spent_points"]) + 2) < 20: #only enough points left to raise st/ht
      if chance > .8: return # Prevent this from happening a bunch
      choice = random.choice(["HT", "ST"])
    elif chance < 0.5001:
      if self.getChoices()["pa"]:
        choice = self.getChoices()["pa"]
      else:
        for skill in self.skills["skills"]:
          try:
            attrs[skill[1]] += 1
          except KeyError:
            attrs[skill[1]] = 1
        high_attr = max(attrs.iteritems(), key=operator.itemgetter(1))[0]
        if high_attr in primary_attributes:
            choice = high_attr
    elif tertiary and secondary:
      this_choice = random.random()
      if this_choice > .4:
        choice = secondary
      else: choice = tertiary
    elif secondary:
      if chance > .6:
        choice = secondary
    elif tertiary:
      if chance > .6:
        choice = secondary
    if not choice: 
      choice = random.choice(["ST", "HT", "IQ", "DX"])
    point_total = int(self.misc["total_points"] + self.disadvantages["disadvantage_limit"])
    divisor_function = round(sum(0.03 for unused in range(point_total)))
    random_mod = [-2, -1, 0, 1]
    max_attr = 10 + (point_total / (40 + divisor_function)) + random.choice(random_mod)
    if self.basic_attributes[choice] < max_attr: #<--- max possible attribute
      if self.basic_attributes[choice] < self.getBaseStats()[choice]:
        self.updateAttrPoints(choice, 1, True)
      else:
        self.updateAttrPoints(choice, 1)
      Print("increasing",choice)
      self.basic_attributes[choice] += 1

  def decreaseRandomAttribute(self):
    """Picks one of the lowest attributes and reduces it by 1."""
    primary_stats = ["ST", "DX", "IQ", "HT"]
    for stat in self.primary_attributes.values():
      if stat in primary_stats:
        primary_stats.remove(stat)
    if len(primary_stats) == 1:
      if random.random() > .4: return # prevents dumpstat of 7 if only one can be lowered
    stats = {}
    for k,v in self.basic_attributes.items():
      if k in primary_stats:
        stats[k] = v
    low = [k for k, v in stats.items() if not any(y < v for y in stats.values())]
    chance = random.random()
    if chance > .7:
      choice = random.choice(primary_stats)
    elif len(low) == 1:
      if len(stats) > 1:
        stats.pop(low[0])
      low.append(min(stats, key=stats.get))
      choice = random.choice(low)
    else:
      choice = random.choice(low)
    if self.basic_attributes[choice] > 7: # <--- Minimum possible stat
      if self.basic_attributes[choice] > self.getBaseStats()[choice]:
        Print(choice, self.basic_attributes[choice] , self.getBaseStats()[choice])
        self.updateAttrPoints(choice, -1, True)
      else:
        Print(choice, self.basic_attributes[choice] , self.getBaseStats()[choice])
        self.updateAttrPoints(choice, -1)
      Print("decreasing",choice)
      self.basic_attributes[choice] -= 1

  def pickAdvantage(self, advantages_list):
    """Picks an advantage! Yaaaayy!
    Args:
      advantages_list: a list of advantages filtered by choice for X/Sup
    """      
    pa = self.primary_attributes["pa"]
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
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 636")
      if random.random() > .05:
        if ideal_list:
          chosen_advantage = random.choice(ideal_list)[:]
        else:
          chosen_advantage = random.choice(pa_based_list)[:]
      else:
        aux_counter = 0
        while aux_counter < 1000:
          aux_counter +=1
          if aux_counter > 998:Print("out of control while loop line 646")
          chosen_advantage = random.choice(advantages_list)[:]
          if chosen_advantage[0] not in [i[0] for i in self.advantages["advantages"]]:
            break
      points = parse(chosen_advantage[3])
      if points < int(self.misc["spent_points"]) + 3:
        break

    self.updatePoints(points)
    chosen_advantage[3] = points
    self.advantages["advantages"].append(chosen_advantage)

  def pickDisadvantage(self, disadvantages_list):
    """Picks a disadvantage!.. awh shucks.
    Args:
      disadvantages_list: a list of disadvantages filtered by choice for X/Sup
    """
    pa = self.primary_attributes["pa"]
    if pa in ["HT", "ST", "DX"]:
      attr_type = random.choice(["M", "Soc"])
    else: 
      attr_type = "P"
    if self.pickQuirks():
      return
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 712")
      if random.random() > .05:
        pa_based_list = [i for i in disadvantages_list if i[1] == attr_type and i[0] not in [
            name[0] for name in self.disadvantages["disadvantages"]]]
        if len(pa_based_list) == 0:
          chosen_disadvantage = random.choice([i for i in disadvantages_list if i[0] not in [
              name[0] for name in self.disadvantages["disadvantages"]]])
        else:
          chosen_disadvantage = random.choice(pa_based_list)[:]
      else:
        aux_counter = 0
        while aux_counter < 1000:
          aux_counter +=1
          if aux_counter > 998:Print("out of control while loop line 725")
          chosen_disadvantage = random.choice(disadvantages_list)[:]
          if chosen_disadvantage[0] not in [i[0] for i in self.disadvantages["disadvantages"]]:
            break
      
      points = parse(chosen_disadvantage[3])
      if self.checkDisadvantageLimit(points):
        break

    self.updatePoints(points)
    chosen_disadvantage[3] = points
    self.disadvantages["disadvantages"].append(chosen_disadvantage)

  def pickQuirks(self):
    """Method for picking quirks when about out of points and disadvantage room"""
    wiggle_room = int(self.disadvantages["disadvantage_limit"]) - int(self.disadvantages["disadvantage_points"])
    if self.misc["spent_points"] < 0:
      if wiggle_room <= 5:
        for unused_point in range(wiggle_room):
          Print("points left:",self.misc["spent_points"], "assigning quirk")
          self.updatePoints(-1)
          self.disadvantages["disadvantages"].append(
              ["Quirk", "M/P/Soc", "-", -1, "162"])
          if self.misc["spent_points"] == 0:
            return True

  def pickSpell(self, potential_spell=[], limiter=0):
    """Picks spells, filters for prerequisite spells and tries to get them as well.
    Args:
      potential_spell: list of a spell to try to pick (like a prerequisite)
      limiter: int of 10 minus how many times to try to pick a spell before giving up
    Returns:
      True: returns true if there are no more spells to pick from, otherwise no return
    """
    # Some spells keep getting picked but prereqs can't be met
    not_gonna_happen = []
    for spell_name, times_picked in self.fool_me["speller"].items():
      if times_picked > 8:
        not_gonna_happen.append(spell_name)
    if potential_spell and potential_spell[0] in not_gonna_happen:
      potential_spell = []
    Print(not_gonna_happen)

    # Build list of spells to pick from
    spell_list = []
    if not self.spells["spells"]:
      potential_spell_list = [i[:] for i in SPELL_LIST[:]]
    else:
      potential_spell_list = [
          hocus[:] for hocus in SPELL_LIST if not [
          x for x in self.spells["spells"] if x[0] == hocus[0]] and not [
          y for y in not_gonna_happen if y == hocus[0]]]
    if self.spells["spell_colleges"]:
      for spell in potential_spell_list:
        if spell[3] in self.spells["spell_colleges"]:
          spell_list.append(spell)
    else:
      spell_list = potential_spell_list 
    Print("Choosing from spells")
    if not spell_list: return True
    if self.spells["spells"] and potential_spell and [
        i for i in self.spells["spells"] if potential_spell[0] == i[0]]:
      potential_spell = []

    # Try 10 times to pick a spell (unless limiter passed only to try to pick a prereq)
    spell_choice = []
    get_prereq = []
    needs_prereq = []
    while limiter < 10:
      limiter += 1        
      check = True
      if not potential_spell:
        potential_spell = random.choice(spell_list)
      Print(potential_spell)
      prereqs = potential_spell[-1]
      Print(prereqs)
      elements = prereqs.split(", ")

      for prereq in elements:
        # This prerequisite is for Magery level
        if "Magery" in prereq:
          level_points = (int(prereq.split(" ")[-1]) * 10) + 5
          for ad in self.advantages["advantages"]:
            if "Magery" in ad[0]:
              if ad[3] < level_points:
                check = False; break

        # This prerequisite is an existing spell
        elif [i for i in SPELL_LIST if i[0] == prereq]:
          if not self.spells["spells"]: check = False; break
          if not [i for i in self.spells["spells"] if i[0] == prereq]:
            get_prereq = [i for i in SPELL_LIST if i[0] in prereq]
            needs_prereq = potential_spell
            check = False; break

        # This prerequisite requires x amount of spells in a college
        elif "++" in prereq:
          if not self.spells["spells"]: check = False; break
          quantity, college = prereq.replace("++","").split(" ")
          counter = 0
          for spell in self.spells["spells"]:
            if college in spell[3]:
              counter += 1
          if counter < int(quantity):
            check = False; break

        # This prerequisite requires spells from x colleges...ugh really? sigh
        elif "colleges" in prereq:
          if not self.spells["spells"]: check = False; break
          amount = prereq.split(" ")[0]
          colleges = set([])
          for spell in self.spells["spells"]:
            colleges.add(spell[3])
          if len(colleges) < int(amount):
            check = False; break

        # This prerequisite requires an IQ at a certain level
        elif "IQ" in prereq:
          needed_amount = prereq.split(" ")[-1]
          if self.basic_attributes["IQ"] < int(needed_amount):
            check = False; break

        # There are only two spells that have an 'or' so this check is mostly situational
        elif " or " in prereq:
          if not self.spells["spells"]: check = False; break
          option_one, option_two = prereq.split(" or ")
          if option_one not in [i[0] for i in self.spells["spells"]]:
            option_one = False
          if not option_one:
            if option_two not in [i[0] for i in self.spells["spells"]]:
              counter = 0
              for spell in self.spells["spells"]:
                if "Earth" in spell[3]:
                  counter += 1
              if counter < 4: check = False; break

        # For a spell requiring x amount of spells in total
        elif "other" in prereq:
          number = int(prereq.split(" ")[0])
          if number > len(self.spells["spells"]):
            check = False; break

      # We have a spell that passes all prerequisite checks, adding it and all done
      if check:
        limiter += 50
        spell_choice = self.setSkillLevel(potential_spell[:])
        self.spells["spells"].append(spell_choice)
      else:
        potential_spell = []

    # Grabs prereq spell (pulled from loop to prevent picking trees of spells at a time)
    if needs_prereq:
      try:
        self.fool_me["speller"][needs_prereq[0]] += 1
      except KeyError:
        self.fool_me["speller"][needs_prereq[0]] = 1
      if get_prereq and self.misc["spent_points"] > -3:
        self.pickSpell(get_prereq[0], 9)

  @Memoize
  def generatePsiPowers(self):
    """Generates a list of psionic advantages.
    Returns:
      psionic_ads: A list of all psionic power advantages"""
    psionic_powers = ["Antipsi", "Esp", "Psychic Healing",
                      "Psychokinesis", "Telepathy", "Teleportation"]
    psionic_ads = []
    for adv in ADVANTAGES_LIST[:]:
      if any(i in psionic_powers for i in adv[-1] if i in self.skills["categories"]):
        psionic_ads.append(adv[:])

    return psionic_ads

  def pickPsi(self):
    """
    """
    psionic_powers = self.generatePsiPowers()
    available = [power for power in psionic_powers if power[0] not in (
                    [current[0] for current in self.advantages["advantages"]])]
    psionic_talents = ["Esp", "Psychic Healing",
                         "Psychokinesis", "Telepathy", "Teleportation"]
    chance = random.random()
    picked = None
    if not any(i in self.advantages["advantages"] for i in available): # No powers yet
      chance += 1
    if self.misc["spent_points"] < 15: # Check for enough points to buy a power
      chance -= 2
    if chance > .7: # Pick a psionic advantage
      counter = 0
      while True:
        counter += 1
        if counter > 50:
          Print("Failed to pick a psionic advantage!")
          return
        picked = random.choice(available)
        if len(psionic_talents) < 6:
          psionic_talents.append("Antipsi")
        points = int(round(parse(picked[3]) * .9)) # Sets points and applies psionic 10% discount
        if points > self.misc["spent_points"] + 3:
          continue
        else:
          break
      self.updatePoints(points)
      picked[3] = points
      cat = [i for i in picked[-1] if i in psionic_talents][0]
      picked[0] = "%s (%s)" % (picked[0], cat)
      self.advantages["advantages"].append(picked)

    else: # Raise a talent level
      talent = random.choice(
                   [i for i in psionic_talents if i in self.skills["categories"]])
      try:
        self.advantages["talents"][talent] += 1
      except KeyError:
        self.advantages["talents"][talent] = 1

      self.updatePoints(5)

  def runCharacterBuildLoop(self):
    """Runs the loop that picks skills/(dis)advantages and in/decreases attributes."""
    advantage_list = [
        i for i in ADVANTAGES_LIST[:] if i[2] in self.advantages["adv_types"]]
    disadvantages_list = [
        i for i in DISADVANTAGES_LIST[:] if i[2] in self.disadvantages["disadv_types"]]
    counter = 0
    psionic_powers = ["Antipsi", "Esp", "Psychic Healing",
                      "Psychokinesis", "Telepathy", "Teleportation"]
    stop_picking_spells = False
    stop_skills = 0
    while self.misc["spent_points"] > 0 and counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 809")
      skill_points = sum([n[-1] for n in self.skills["skills"]])
      spend_limit = int(self.misc["spent_points"]) + 3
      if [i for i in self.advantages["advantages"] if "Magery" in i[0]]:
        choice = random.randint(40, 130)
      else:
        choice = random.randint(20, 100)

      # Pick the first skill to get primary attributes and all that jolly good stuff set
      if not self.skills["skills"]:
        Print("points left:",self.misc["spent_points"], "picking first skill")
        first_skill = self.pickSkill()
        if not first_skill: continue
        self.skills["skills"].append(first_skill)
      # Add a psionic power
      elif choice > 95 and choice < 100 and any(
          i in psionic_powers for i in self.skills["categories"]):
        if self.misc["spent_points"] > 5:
          self.pickPsi()
      # Add a spell
      elif choice > 100 and not stop_picking_spells:
        Print("points left:",self.misc["spent_points"], "picking SPELL")
        stop_picking_spells = self.pickSpell()
      # Add a skill
      elif stop_skills < 10 and choice < 89 and self.skills["skill_limit"] > skill_points:
        raw_skill = self.pickSkill()
        if not raw_skill:
          stop_skills += 1
          Print("attempted to pick skill and failed")
          continue
        Print("points left:",self.misc["spent_points"], "just picked a skill")
        self.skills["skills"].append(raw_skill)
      # Increase a stat
      elif (choice > 88) and (choice < 93) and spend_limit > 10:
        Print("points left:",self.misc["spent_points"], "raising stat")
        self.increaseRandomAttribute()
      # Add an advantage
      elif (choice > 92) and (choice < 94):
        Print("points left:",self.misc["spent_points"], "picking advantage")
        self.pickAdvantage(advantage_list)
      # Decrease a stat
      elif (choice > 93) and (choice < 95) and self.checkDisadvantageLimit(-20):
        Print("points left:",self.misc["spent_points"], "decreasing stat")
        self.decreaseRandomAttribute()
      # Add a disadvantage
      elif (choice > 94) and (choice < 96) and self.checkDisadvantageLimit(-10):
        Print("points left:",self.misc["spent_points"], "picking disadvantage")
        self.pickDisadvantage(disadvantages_list)
      # Add a disadvantage when out of points or at 0 and still have disadvantage points
      wiggle_room = int(self.disadvantages["disadvantage_limit"]) - int(
                        self.disadvantages["disadvantage_points"])
      aux_counter = 0
      while self.misc["spent_points"] < 0:
        Print("points left:",self.misc["spent_points"], "picking disadvantage!", wiggle_room)
        aux_counter += 1
        if aux_counter > 998:Print("out of control while loop line 857");break
        self.pickDisadvantage(disadvantages_list)
        wiggle_room = int(self.disadvantages["disadvantage_limit"]) - int(
                          self.disadvantages["disadvantage_points"])
      if self.misc["spent_points"] == 0 and wiggle_room > 5:
        Print("picking disadvantage(0 points and still some wiggle room)", wiggle_room)
        self.pickDisadvantage(disadvantages_list)

  def build(self):
    """Assembles all of the above madness into a character."""
    self.getChoices()
    self.getBaseStats()
    self.chooseSkillCategories()
    self.getMustHaves()
    # Sets height, weight, appearance and physical build
    self.setAppearance()
    # Sets starting wealth attributes
    self.setWealth()
    # Configures all other attributes of the character
    counter = 0
    while counter < 1000:
      counter +=1
      if counter > 998:Print("out of control while loop line 876")
      if counter > 1: Print("BWAH FAILED PREREQS(removing quirks and build looping again")
      self.runCharacterBuildLoop()
      self.updateSecondaryAttributes()
      self.updateSkillLevels()
      if self.auditSkillPrereqs():
        break
    self.updatePsiTalents()
    self.cleanAds(self.advantages["advantages"])
    self.cleanAds(self.disadvantages["disadvantages"])
    self.cleanSkills()
    self.spells["spells"] = self.formattedItems(self.spells["spells"], SPELL_HEADER)
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

