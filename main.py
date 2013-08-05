import webapp2
import charbuilder
import sys
import traceback


def getText(file):
  with open(file, "r") as f:
    return f.read().replace("\n", "")


HTML = {"main_page": getText("main_page.html")}


def mergeDicts(master_dict):
  new_dict = []
  for dictionary in master_dict.keys():
    if not dictionary:
      continue
    new_dict.extend(master_dict[dictionary].items())
  return dict(new_dict)

class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    try:
      new_character = charbuilder.CharacterBuilder(100)
      self.response.write(HTML["main_page"] % (mergeDicts(new_character.__dict__)))
    except Exception as e:
      self.response.write(traceback.format_exc())
  

handlers = [('/', MainPage)]

application = webapp2.WSGIApplication(handlers, debug=True)















