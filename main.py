import webapp2
import charbuilder
import traceback
import skills


def getFile(_file):
  with open(_file, "r") as f: return f.read().replace("\n", "")
HTML = {"main_page": getFile("main_page.html")}


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
      self.response.write(HTML["main_page"] % (
                                  mergeDicts(charbuilder.CharacterBuilder(100).__dict__)))
    except Exception:
      self.response.write(traceback.format_exc())
  

handlers = [('/', MainPage)]
application = webapp2.WSGIApplication(handlers, debug=True)

  












