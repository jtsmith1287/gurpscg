import webapp2
from google.appengine.ext import db
import logging
import charbuilder
import traits
import traceback
import random
import string


instance_key = "".join(
    (random.choice(string.ascii_uppercase + string.digits) for i in xrange(25)))

def getFile(_file):
  with open(_file, "r") as f: return f.read().replace("\n", "")

HTML = {"main_page": getFile("main_page.html"),
        "creation_page": getFile("creation_page.html")}

def mergeDicts(master_dict):
  new_dict = []
  for dictionary in master_dict.keys():
    if not dictionary:
      continue
    new_dict.extend(master_dict[dictionary].items())

  return dict(new_dict)


class Parameters(db.Model):
  
  parameters = db.StringProperty()
  order = db.DateTimeProperty(auto_now=True)
  instance_key = db.StringProperty()


class MainPage(webapp2.RequestHandler):

  fields = {"cat_checkboxes": "",
            "spell_checkboxes": ""}

  def get(self):
    """
    """
    self.response.headers['Content-Type'] = 'text/html'  # tells the page to load as html instead of plain text
    try:
      self.configureCatBoxes()
      self.configureSpellCollegeCheckboxes()
      self.response.write(HTML["main_page"] % self.fields)  # renders the main_page.html contents
    except Exception:
      self.response.write(traceback.format_exc())  # if there was an error, write that instead of the main_page

  def configureSpellCollegeCheckboxes(self):

    spell_colleges = {"MC": "Mind Control",
                      "Meta": "Meta",
                      "L/D": "Light & Darkness",
                      "Move.": "Movement",
                      "BC": "Body Control",
                      "Fire": "Fire",
                      "P/W": "Protection & Warning",
                      "Air": "Air",
                      "Water": "Water",
                      "Ench.": "Enchantment",
                      "C/E": "Communication & Emptahy",
                      "Healing": "Healing",
                      "Know.": "Knowledge",
                      "Earth": "Earth",
                      "Gate": "Gate",
                      "Necro.": "Necromantic"}
    
    checkbox_html = '<input type="checkbox" name="spell_colleges" value="%s"> %s'
    column = 0
    complete_html = "<table>"
    for cat in sorted(spell_colleges.keys()):
      if column > 5:
        column = 0
      if column == 0:
        complete_html += "<tr>"  # starts a new table row
      y = checkbox_html % (cat, spell_colleges[cat])  # this puts whatever the current category is as the value and text to display
      complete_html += "<td> %s </td>" % (y)  # puts the entire line as column with the td tag
      column += 1  # go to the next column
    complete_html += "</table>"  # close the table
    self.fields["spell_checkboxes"] = complete_html

  def configureCatBoxes(self):

    psionic_powers = ["Antipsi", "Esp", "Psychic Healing", 
                      "Psychokinesis", "Teleportation", "Telepathy"]
    power_cats = []
    checkbox_html = '<input type="checkbox" name="cat_type" value="%s"> %s'
    column = 0
    complete_html = "<table>"
    for cat in sorted(traits.traits.SKILL_CATEGORIES):
      if cat in psionic_powers:
        power_cats.append(cat)
        continue
      if column > 5:
        column = 0
      if column == 0:
        complete_html += "<tr>"  # starts a new table row
      y = checkbox_html % (cat, cat)  # this puts whatever the current category is as the value and text to display
      complete_html += "<td> %s </td>" % (y)  # puts the entire line as column with the td tag
      column += 1  # go to the next column
    complete_html += "</table>"
    complete_html += "<br><b>Psionic Powers</b><br>"
    complete_html += "<table>"
    column = 0
    for cat in power_cats:
      if column > 5:
        column = 0
      if column == 0:
        complete_html += "<tr>"  # starts a new table row
      y = checkbox_html % (cat, cat)  # this puts whatever the current category is as the value and text to display
      complete_html += "<td> %s </td>" % (y)  # puts the entire line as column with the td tag
      column += 1
    complete_html += "</table>"
    self.fields["cat_checkboxes"] = complete_html

  def post(self):
    """
    """
    self.response.headers['Content-Type'] = 'text/html'
    try:
      try:
        fd = self.getRequests()
        logging.info(fd)
        self.saveParameters(fd)
      except ValueError:
        fd = self.getParameters()

      new_character = charbuilder.CharacterBuilder(fd)
      # Write the generated character to the page after formatting
      nc = mergeDicts(new_character.__dict__)
      
      self.response.write(HTML["creation_page"] % (nc))
    except:
      self.response.write(traceback.format_exc())

  def getRequests(self):
    """Returns all form data from current set parameters.
    """
    return {"points": int(self.request.get("points")),
            "tl": int(self.request.get("Tech Level")),
            "adv_types": self.request.get_all("adv_type"),
            "disadv_types": self.request.get_all("disadv_type"),
            "d_limit": self.request.get("d_limit"),
            "categories": self.request.get_all("cat_type"),
            "pa": self.request.get("pa"),
            "sa": self.request.get("sa"),
            "ta": self.request.get("ta"),
            "spell_colleges": self.request.get_all("spell_colleges")
            }

  def saveParameters(self, data):
    """
    """
    # convert python dict syntax to a string
    string_data = repr(data)
    new_entity = Parameters()
    new_entity.parameters = string_data
    # save data
    new_entity.put()
    logging.info(instance_key)

  def getParameters(self):
    """
    """
    all_data = Parameters.all()
    all_data.order("-order")
    try:
      fd = eval(all_data.fetch(limit=1)[0].parameters)
    except IndexError:
      fd = None

    return fd


handlers = [("/", MainPage)]

application = webapp2.WSGIApplication(handlers, debug=True)  



