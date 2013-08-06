import webapp2
import charbuilder
import traceback
import logging


def getText(_file):
  with open(_file, "r") as f: return f.read().replace("\n", "")


HTML = {"main_page": getText("main_page.html")}


def mergeDicts(master_dict):
  new_dict = []
  #return dict([master_dict[d].items() for d in master_dict.keys() if d])
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
    except Exception:
      logging.error(traceback.format_exc())
  

handlers = [('/', MainPage)]

application = webapp2.WSGIApplication(handlers, debug=True)

if __name__ == "__main__":
  mergeDicts(charbuilder.CharacterBuilder(100).__dict__)
  
  print "\nApp excecution successful."
  print "You can now run Google App Engine Launcher."














