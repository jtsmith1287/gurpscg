'''
Created on Oct 13, 2013

@author: Justin
'''


class SkillPicker:


  def formattedSkills(self, skill_list):
    """Formats a list of skills into html.
    
    Args:
      skill_list: a list of skills.
    Returns:
      formatted_skills: a string of all skills as html
    """
    #TODO (Justin): Pretty up the html a bit to hide python syntax
    #MAYBE: Somewhere the skill levels need to be added; either here or elsewhere.
    
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
        if cat in skill[-1] and skill not in possible_skills:
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
    skill_difficulty = skill[2]
    # We get the list of possible point costs
    point_table = utils.getColumnFromTable(SKILL_COST_TABLE, "PS")
    # Then we'll get a weighted random point cost from that list
    points_to_spend = point_table[utils.randBiDistrib(point_table, 1.5)]
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

  def pickSkill(self, probable_skills, all_skills):
    """Picks a skill at random from skill_lists.
    
    Args:
      probable_skills: a list of good candidates and other possible skills
    Returns:
      skill: a list that is the chosen skill
    """
    skill = []
    good_candidates = self.getGoodCandidateSkills(probable_skills)
    chance = random.randint(1, 10)
    self.Print("=================================================")
    while not skill:
      if good_candidates and chance > 2:
        skill_list = good_candidates
      elif probable_skills and chance == 1:
        skill_list = probable_skills
      else:
        skill_list = list(all_skills)[1:]
      skill_choice = random.choice(skill_list)[:]
      #self.Print(skill_choice[0])
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

    self.Print(skill)
    return skill

  def updateSkillLevels(self):
    """
    """
    for skill in self.skills["skills"]:
      skill.insert(-1, self.basic_attributes[skill[1]] + skill[-2])


