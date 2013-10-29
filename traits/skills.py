
import os.path

file_path = os.path.join(os.path.dirname(__file__),"skills.dat")

with open(file_path, "r") as f:
  DATA = f.readlines()

SKILL_CATEGORIES = set([])

SKILLS = []

for line in DATA:
  skill = eval(line)
  SKILLS.append(skill)
  for cat in skill[-1]:
    SKILL_CATEGORIES.add(cat)