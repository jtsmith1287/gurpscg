'''
Created on Aug 5, 2013

@author: Justin
'''

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


for i, line in enumerate(data["advantages"]):
  adv = eval(line)
  if type(adv[-1]) == type([]):
    adv.pop(-2)
  print adv
  data["advantages"][i] = repr(adv) + "\n"

for i, line in enumerate(data["disadvantages"]):
  adv = eval(line)
  if type(adv[-1]) == type([]):
    adv.pop(-2)
  print adv
  data["disadvantages"][i] = repr(adv) + "\n"



"""with open(gdats["advantages"], "w") as f:
  f.writelines(data["advantages"])
  print "saved advantages"
with open(gdats["disadvantages"], "w") as f:
  f.writelines(data["disadvantages"])
  print "Saved disadfdksfjkldjs stuff"""

