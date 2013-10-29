import webapp2
from google.appengine.ext import db
import logging
import charbuilder
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

  def get(self):
    """
    """
    self.response.headers['Content-Type'] = 'text/html'
    try:
      self.response.write(HTML["main_page"])
    except Exception:
      self.response.write(traceback.format_exc())

  def post(self):
    """
    """
    self.response.headers['Content-Type'] = 'text/html'
    try:
      try:
        fd = self.getRequests()
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



