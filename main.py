import webapp2
import charbuilder
import traceback


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
      self.response.write(traceback.format_exc())
  

handlers = [('/', MainPage)]

application = webapp2.WSGIApplication(handlers, debug=True)


if __name__ == "__main__":
  character = charbuilder.CharacterBuilder(100)
  c = mergeDicts(character.__dict__)
  
#=========================================================================================
#   for k,v in character.skills.items():
#     if k == "skills":
#       for i in character.skills[k].split("<br>"):
#         print i
#       continue
#     print k, v
#   print
#   print "\nApp excecution successful."
#   print "You can now run Google App Engine Launcher."
# 
#=========================================================================================












