
import os.path

files = ["skills.gdat", "advantages.gdat", "disadvantages.gdat", "spells.gdat"]
data = {}

for gdat in files:
  file_path = os.path.join(os.path.dirname(__file__), gdat)
  with open(file_path, "r") as f:
    data[gdat] = f.readlines()

SKILL_CATEGORIES = set([])
SKILLS = []
ADVANTAGES_LIST = []
DISADVANTAGES_LIST = []
SPELL_LIST = []

for line in data["skills.gdat"]:
  item = eval(line)
  SKILLS.append(item)
  for cat in item[-1]:
    SKILL_CATEGORIES.add(cat.strip("---"))
for line in data["advantages.gdat"]:
  item = eval(line)
  ADVANTAGES_LIST.append(item)
  for cat in item[-1]:
    SKILL_CATEGORIES.add(cat.strip("---"))
for line in data["disadvantages.gdat"]:
  item = eval(line)
  DISADVANTAGES_LIST.append(item)
for line in data["spells.gdat"]:
  item = eval(line)
  SPELL_LIST.append(item)

