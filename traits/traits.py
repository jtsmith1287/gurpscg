
import os.path

files = ["skills.gdat", "advantages.gdat", "disadvantages.gdat"]
data = {}

for gdat in files:
  file_path = os.path.join(os.path.dirname(__file__), gdat)
  with open(file_path, "r") as f:
    data[gdat] = f.readlines()

SKILL_CATEGORIES = set([])
SKILLS = []
ADVANTAGES_LIST = []
DISADVANTAGES_LIST = []

for line in data["skills.gdat"]:
  item = eval(line)
  SKILLS.append(item)
  for cat in item[-1]:
    SKILL_CATEGORIES.add(cat)
for line in data["advantages.gdat"]:
  item = eval(line)
  ADVANTAGES_LIST.append(item)
for line in data["disadvantages.gdat"]:
  item = eval(line)
  DISADVANTAGES_LIST.append(item)

#print SKILL_CATEGORIES
#print SKILLS
#print ADVANTAGES_LIST
#print DISADVANTAGES_LIST
