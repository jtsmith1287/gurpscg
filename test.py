'''
Created on Aug 5, 2013

@author: Justin
'''

import random
import os
import glob

EXT = ".gdat"
GDAT_DIR = "traits"

current_dir = os.path.dirname(__file__)
traits_dir = os.path.join(current_dir, GDAT_DIR)

for root, dir, files in os.walk(traits_dir):
  for file_ in files:
    if file_.endswith(EXT):
      print os.path.join(root, file_)