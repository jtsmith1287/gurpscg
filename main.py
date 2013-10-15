import webapp2
import charbuilder
import traceback


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

class MainPage(webapp2.RequestHandler):

  def get(self):
    self.response.headers['Content-Type'] = 'text/html'
    try:
      self.response.write(HTML["main_page"])
    except Exception:
      self.response.write(traceback.format_exc())


class GenerationPage(webapp2.RequestHandler):

  def post(self):
    self.response.headers['Content-Type'] = 'text/html'
    try:
      fd = {"points": int(self.request.get("points")),
            "tl": int(self.request.get("Tech Level")),
            "adv_types": self.request.get("mundane", "exotic", "supernatural")
            }
      new_character = charbuilder.CharacterBuilder(fd)
      # Write the generated character to the page after formatting
      nc = mergeDicts(new_character.__dict__)
      self.response.write(HTML["creation_page"] % (nc))
    except Exception:
      self.response.write(traceback.format_exc())
    

handlers = [("/", MainPage),
            ("/generated", GenerationPage)]
application = webapp2.WSGIApplication(handlers, debug=True)

if __name__ == "__main__":
  charbuilder.CharacterBuilder(500)
  



