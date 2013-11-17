import os

EXT = ".gdat"
GDAT_DIR = "traits"
data = {}
gdats = {}
current_dir = os.path.dirname(__file__)
traits_dir = os.path.join(current_dir, GDAT_DIR)
for root, dir, files in os.walk(traits_dir):
  for file_ in files:
    if file_.endswith(EXT):
      gdat_name = file_.split(".")[0]
      gdats[gdat_name] = os.path.join(root, file_)
      with open(gdats[gdat_name], "r") as file:
        data[gdat_name] = file.readlines()
        
for idx,i in enumerate(data['skills']):
  skill = eval(i)
  skill[3][1] = 13
  data["skills"][idx] = repr(skill) + "\n"
with open(gdats["skills"], "w") as f:
  f.writelines(data["skills"])