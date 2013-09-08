'''
Created on Jul 31, 2013

@author: Justin & Theophilus
'''

from tables import *
from skills import *
import operator
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
    self.basic_attributes = {"ST": 10, "DX": 10,   "IQ": 10,  "HT": 10,
                             "HP": 10, "Will": 10, "Per": 10, "FP": 10}
    self.secondary_attributes = {}
    self.wealth = {"TL": 8}
    self.appearance = {}
    self.encumbrance = {}
    self.skills = {"skills": []}
    self.advantages = {}
    self.disadvantages = {"disadvantage_limit": random.randint(0, points/2)}

    self.build()
  
  def updatePoints(self, points, stat=None):

    if stat:
      print "%s change by %s<br>" %(stat, points)
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
    """Randomly selects starting wealth and status.

    Returns:
      wealth: a dictionary containing all wealth attributes for the character
    """

    wealth = {}
    wealth_status = WEALTH_TABLE[0][utils.randWeight(WEALTH_TABLE[0])]
    starting_wealth = STARTING_WEALTH[self.wealth["TL"]]
    wealth_details = utils.getColumnFromTable(WEALTH_TABLE, wealth_status)

    wealth["starting_cash"] = "{:,}".format(int(starting_wealth * wealth_details[1]))
    wealth["status"] = wealth_status
    wealth["status_description"] = wealth_details[0]
    self.updatePoints(wealth_details[-1])
    
    return wealth

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

  def chooseSkillCategories(self):
    """Chooses between 1 and 3 skill categories.
    
    Returns:
      skill_cats: a list of skill categories.
    """

    # The key == how many skill categories the character will have.
    template = {1: "Focused",
                2: "Specialized",
                3: "Blended"}
    skill_cats = []
    for i in xrange(random.randint(1, 3)):
      while True:
        cat = random.choice(SKILL_CATEGORIES)
        if cat not in skill_cats:
          skill_cats.append(cat)
          break
    self.skills["focus"] = template[len(skill_cats)]
    
    return skill_cats

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
    max_attr =  random.choice(max_attrs)

    return max_attr

  def formattedSkills(self, skill_list):
    """Formats a list of skills into html.
    
    Args:
      skill_list: a list of skills.
    Returns:
      formatted_skills: a string of all skills as html
    """
    #TODO (Justin): Pretty up the html a bit to hide python syntax
    #MAYBE: Somwewhere the skill levels need to be added; either here or elsewhere.
    
    new_skill_list = []
    for skill in skill_list:
      formatted_skill = []
      for item in skill:
        formatted_skill.append("<td> %s </td>" %(item))
      new_skill_list.append("<tr> %s </tr>" %("".join(formatted_skill)))

    header = "<th>Name</th><th>Attribute</th><th>Difficulty</th>"\
             "<th>TL</th><th>Page</th><th>R.Level</th><th>Level</th>"\
             "<th>Points</th>"
    table_tag = "<table border=\"5\">%s%s</table>"
    formatted_skills = table_tag %(header, "".join(new_skill_list))
    return formatted_skills

  def getPossibleSkills(self, skills):
    """Creates a list of likely skills for choosing the character's skills.

    Returns:
      skill_lists: a list of probable skills
    """
    possible_skills = []

    for skill in skills[1:]:
      for cat in self.skills["skill_categories"]:
        if cat == skill[-1] and skill not in possible_skills:
          
          # [-1]: references category of the skill
          possible_skills.append(skill)

    return possible_skills

  def getGoodCandidateSkills(self, possible_skills):
    """Generates a list of skills based on a given attribute.

    Args:
      possible_skills: list of the skills that match the characters categories.
    Returns:
      good_candidates: list of skills that match the primary attribute.
    """
    good_candidates = []
    p_attr = self.getPrimaryAttribute()
    for skill in possible_skills:
      if p_attr in skill[1] and skill not in good_candidates: 
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
    i = SKILLS.index(skill)
    skill_difficulty = skill[2]
    # We get the list of possible point costs
    point_table = utils.getColumnFromTable(SKILL_COST_TABLE, "PS")
    # Then we'll get a weighted random point cost from that list
    points_to_spend = point_table[utils.randBiDistrib(point_table, 2)]
    # We'll need the column for where we're going to get the relative skill level
    # based on the already chosen point cost
    table_index = SKILL_COST_TABLE[0].index(skill_difficulty)
    # This is where we get the row for all possible difficulties associoated with
    # that point cost
    skill_levels = utils.getRowFromTable(SKILL_COST_TABLE, points_to_spend)
    # And now we actually get our skill level and we'll replace the skill
    # categories with the relative level, and then extend the skill to show the
    # actual level (which is the base attribute + the relative level
    skill_level = skill_levels[table_index]
    skill[-1] = skill_level
    skill.extend([self.basic_attributes[skill[1]] + skill_level,
                  points_to_spend])
    self.updatePoints(points_to_spend)


    return skill

  def pickSkill(self, probable_skills, all_skills):
    """Picks a skill at random from skill_lists.
    
    Args:
      probable_skills: a list of good candidates and other possisble skills
    Returns:
      skill: a list that is the chosen skill
    """
    skill = []
    good_candidates = self.getGoodCandidateSkills(probable_skills)
    chance = random.randint(1, 10)
    while not skill:
      if good_candidates and chance > 2:
        skill_list = good_candidates
      elif probable_skills and chance == 1:
        skill_list = probable_skills
      else:
        skill_list = list(all_skills)[1:]
      skill_choice = random.choice(skill_list)
      if skill_choice in self.skills["skills"]:
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
    # Set the level of a copy of the skill and return the copy
    skill = self.setSkillLevel(skill[:])

    return skill

  def updateAttrPoints(self, stat, mod):
    """
    """
    print stat
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

    self.updatePoints(cost, stat)

  def increaseAttribute(self):
    """
    """
    attrs = {}
    for skill in self.skills["skills"]:
      try:
        attrs[skill[1]] += 1
      except KeyError:
        attrs[skill[1]] = 1
    high_attr = max(attrs.iteritems(), key=operator.itemgetter(1))[0]
    chance = random.random()
    if chance < 0.81:
      self.updateAttrPoints(high_attr, 1)
      self.basic_attributes[high_attr] += 1
    else:
      attr_choices = ["ST", "HT", "IQ", "DX"]
      attr_choices.remove(high_attr)
      highestestest_attr = random.choice(attr_choices)
      self.updateAttrPoints(highestestest_attr, 1)
      self.basic_attributes[highestestest_attr] += 1

  def build(self):
    """Assembles all attributes of the character.
    """
    all_skills = list(SKILLS)[:]
    self.setAppearance()
    self.wealth.update(self.setWealth())    
    self.skills["skill_categories"] = self.chooseSkillCategories()
    skill_list = self.getPossibleSkills(all_skills)

    num_advantages = 0
    num_attrs = 0
    for i in xrange(15):
      choice = random.randint(1, 3)
      if choice == 1:
        self.skills["skills"].append(self.pickSkill(skill_list, all_skills))
      if choice == 2:
        #increase a stat
        if not self.skills["skills"]:
          continue
        self.increaseAttribute()
      if choice == 3:
        #add an advantage
        num_advantages += 1

    
    #if spent_points > point total: pickDisadvantage(point_limit)
    
    self.skills["skills"] = self.formattedSkills(self.skills["skills"])
    self.calculateMisc()

    self.advantages["a_notice"] = num_advantages
    self.disadvantages["d_notice"] = "Feature coming soon!"




