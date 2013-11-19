'''
Created on Oct 25, 2013

@author: Justin
'''
import Tkinter as tk
import tkMessageBox as tkmsg
import re
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


class Application(tk.Frame):
  
  def __init__(self, bg_color, master = None):
    tk.Frame.__init__(self, master,
                      bg = bg_color)

    # Allow for window resizing
    top = self.winfo_toplevel()
    top.rowconfigure(0, weight = 1)
    top.columnconfigure(0, weight = 1)
    self.rowconfigure(0, weight = 1)
    self.columnconfigure(0, weight = 1)
    self.grid(sticky = tk.N + tk.S + tk.E + tk.W)

    self.bg = bg_color
    self.active_list = None
    self.active_scrollbar = None
    self.checkboxes = {}
    self.checked_boxes = []
    self.just_checked = None
    self.item = None
    self.item_index = None
    self.stats = tk.StringVar()
    self._run()

  def listboxSelect(self, listbox, index):

    listbox.select_clear(tk.ACTIVE)
    listbox.activate(index)
    listbox.selection_set(tk.ACTIVE)
    listbox.see(index + 10)

  def _populateSkillList(self):
    
    self.item_count = 0
    self.incomplete_count = 0
    self.skill_list_listbox.delete(0, tk.END)
    self.skill_list_listbox.delete(tk.END)
    for i in sorted(self.skill_list):
      self.item_count += 1
      if i[-1]:
        name = i[0]
      else:
        name = i[0] + " <--- Incomplete!"
        self.incomplete_count += 1
      self.skill_list_listbox.insert(tk.END, name)
    self._updateStatsWidget()

  def _populateAdvantagesList(self):

    self.item_count = 0
    self.incomplete_count = 0
    self.advantages_list_listbox.delete(0, tk.END)
    self.advantages_list_listbox.delete(tk.END)
    for i in sorted(self.advantages_list):
      self.item_count += 1
      if i[-1]:
        name = i[0]
      else:
        name = i[0] + " <--- Incomplete!"
        self.incomplete_count += 1
      self.advantages_list_listbox.insert(tk.END, name)
    self._updateStatsWidget()

  def _populateDisadvantagesList(self):

    self.item_count = 0
    self.incomplete_count = 0
    self.disadvantages_list_listbox.delete(0, tk.END)
    self.disadvantages_list_listbox.delete(tk.END)
    for i in sorted(self.disadvantages_list):
      self.item_count += 1
      if i[-1]:
        name = i[0]
      else:
        name = i[0] + " <--- Incomplete!"
        self.incomplete_count += 1
      self.disadvantages_list_listbox.insert(tk.END, name)
    self._updateStatsWidget()

  def _updateStatsWidget(self):

    stats = "Items: %(item_count)s\nUnconfigured: %(incomplete_count)s" % (
        self.__dict__)
    percent = 100 - int((float(self.incomplete_count) / self.item_count) * 100)
    stats += "\nWinning: %s%%" % percent
    self.stats.set(stats)

  def _configureColsRows(self):

    col, row = self.grid_size()
    for i in range(col):
      self.grid_columnconfigure(i, pad = 20,)
    for i in range(row):
      self.grid_rowconfigure(i, pad = 20,)

  def activateSkillList(self):

    if self.active_list:
      self.active_list.grid_forget()
      self.active_scrollbar.grid_forget()
    self.active_list = self.skill_list_listbox
    self.active_scrollbar = self.skill_list_scrollbar
    self.skill_list_listbox.grid(row = 1,
                                 column = 0,
                                 columnspan = 3,
                                 sticky = tk.N + tk.S + tk.W + tk.E)
    self.skill_list_scrollbar.grid(row = 1,
                                   column = 3,
                                   sticky = tk.N + tk.S + tk.W)
    self._populateSkillList()

  def activateAdvantagesList(self):

    if self.active_list:
      self.active_list.grid_forget()
      self.active_scrollbar.grid_forget()
    self.active_list = self.advantages_list_listbox
    self.active_scrollbar = self.advantages_list_scrollbar
    self.advantages_list_listbox.grid(row = 1,
                                      column = 0,
                                      columnspan = 3,
                                      sticky = tk.N + tk.S + tk.W + tk.E)
    self.advantages_list_scrollbar.grid(row = 1,
                                        column = 3,
                                        sticky = tk.N + tk.S + tk.W)
    self._populateAdvantagesList()

  def activateDisadvantagesList(self):

    if self.active_list:
      self.active_list.grid_forget()
      self.active_scrollbar.grid_forget()
    self.active_list = self.disadvantages_list_listbox
    self.active_scrollbar = self.disadvantages_list_scrollbar
    self.disadvantages_list_listbox.grid(row = 1,
                                 column = 0,
                                 columnspan = 3,
                                 sticky = tk.N + tk.S + tk.W + tk.E)
    self.disadvantages_list_scrollbar.grid(row = 1,
                                   column = 3,
                                   sticky = tk.N + tk.S + tk.W)
    self._populateDisadvantagesList()

  def _newCategory(self):

    self.category_editor_area.grid(column = self.grid_size()[0],
                                   row = 0)
    self.category_entry.grid(row = 1,
                             columnspan = 2,
                             pady = 10,
                             sticky = tk.W + tk.E)
    self.category_submit_button.grid(row = 2,
                                     column = 0,
                                     padx = 5,
                                     sticky = tk.E + tk.W)
    self.category_cancel_button.grid(row = 2,
                                    column = 1,
                                    padx = 5,
                                    sticky = tk.E + tk.W)
    self._configureColsRows()

  def _saveCategory(self):

    new_cat = self.category_entry_var.get().split()
    if new_cat:
      new_cat = " ".join([i[0].upper() + i[1:].lower() for i in new_cat])
      self.item_categories.add(new_cat)
      self.cancel_newCategory()
      self._layoutItemEditorArea()
    else:
      tkmsg.showerror(
          "Type Somethin'", "Sorry, Boss. We can't have nil cats _runnin'round!")

  def cancel_newCategory(self):

    self.category_editor_area.grid_forget()

  def selectItem(self, event = None):

    if event:
      raw_name = event.widget.get(event.widget.curselection()[0])
    else:
      raw_name = self.active_list.get(tk.ACTIVE)
    item_name = raw_name.split(" <--- ")[0].strip()
    self.listbox_position = self.active_list.get(0, tk.END).index(raw_name)
    self.item_type = None
    # Look for item in Skills
    for i in data["skills"]:
      if eval(i)[0] == item_name:
        self.item = eval(i)
        self.item_index = data["skills"].index(i)
        if type(self.item[-3]) == type([]):
          self.skill_prereq_entry_var.set(", ".join(self.item[-3]))
        else:
          self.skill_prereq_entry_var.set("")
        self.item_type = "skills"
        break
    # Look for item in advantages
    for i in data["advantages"]:
      if eval(i)[0] == item_name:
        self.item = eval(i)
        self.item_index = data["advantages"].index(i)
        self.item_type = "advantages"
    # Look for item in disadvantages
    for i in data["disadvantages"]:
      if eval(i)[0] == item_name:
        self.item = eval(i)
        self.item_index = data["disadvantages"].index(i)
        self.item_type = "disadvantages"
    if self.item_type:
      self.skill_editor_area.grid(row = 0,
                                  column = self.grid_size()[0],
                                  sticky = tk.W + tk.E + tk.N + tk.S)
      self._layoutItemEditorArea()
    else:
      self.item = None
      tkmsg.showerror("O_O", "How the ... ")

  def _saveItem(self):

    # Get skill specific data
    if self.item_type == "skills":
      tl_index = 3
      prereqs = self.skill_prereq_entry_var.get().split(", ")
      if prereqs[0] == '':
        prereqs = []
      if len(self.item) == 6:
        self.item.insert(-2, prereqs)
      elif len(self.item) == 7:
        self.item[-3] = prereqs
      else:
        print self.item
    # Get advantage/disadvantage specific data
    else:
      tl_index = 5

    kitties = []
    for cat, check in self.checkboxes.items():
      if check["var"].get() == 1:
        if check["checkbox"]["bg"] == "yellow":
          if "---" not in cat:
            cat = "%s---" % cat
        elif "---" in cat:
          cat.replace("---", "")
        kitties.append(cat)
      self.item[-1] = kitties
    self.item[tl_index][0] = int(self.tech_level_spinbox.get())
    self.item[tl_index][1] = int(self.max_tech_level_spinbox.get())
    data[self.item_type][self.item_index] = str(self.item) + "\n"
    self._cancelItem()
    self.saveData()
    self.updateData()
    self.listboxSelect(self.active_list, self.listbox_position + 1)
    if self.item_type == "skills":
      self._populateSkillList()
    elif self.item_type == "advantages":
      self._populateAdvantagesList()
    else:
      self._populateDisadvantagesList()

  def _cancelItem(self):

    self.item = None
    self.item_index = None
    self.skill_editor_area.grid_forget()
  
  def nextSkill(self):

    active = self.active_list.get(tk.ACTIVE)
    listbox_contents = self.active_list.get(0, tk.END)
    current_pos = listbox_contents.index(active)
    if current_pos + 1 >= 0:
      new_pos = current_pos + 1
      self.listboxSelect(self.active_list, new_pos)
  
  def previousSkill(self):

    active = self.active_list.get(tk.ACTIVE)
    listbox_contents = self.active_list.get(0, tk.END)
    current_pos = listbox_contents.index(active)
    if current_pos + 1 >= 0:
      new_pos = current_pos - 1
      self.listboxSelect(self.active_list, new_pos)

  def searchActiveList(self, event = None):
    
    item_list = self.active_list.get(0, tk.END)
    if event:
      search_term = event.widget.get()
    else:
      search_term = self.searchbar_stringvar.get()
    result = None
    for list_index, word_case in enumerate(item_list):
      word = word_case.lower()
      match = True
      if word == search_term:
        result = word
        break
      if len(word) < len(search_term):
        match = False
        break
      for idx in xrange(len(search_term)):
        if word[idx] != search_term[idx]:
          match = False
      if match:
        result = word
        break
    if result:
      self.listboxSelect(self.active_list, list_index)
    else:
      tkmsg.showerror("Nil Cat!", "That search yielded nothing.")

  def doubleCheck(self):

    last_checked = None
    for cat, data in self.checkboxes.items():
      intvar = data["var"]
      box = data["checkbox"]
      i = intvar.get()
      if cat not in self.checked_boxes:
        if i:
          self.checked_boxes.append(cat)
          last_checked = (box, intvar, cat)
      if cat in self.checked_boxes:
        if not i:
          last_checked = (box, intvar, cat)

    box, intvar, cat = last_checked
    if not intvar.get() and box["bg"] == self.bg:
      box["bg"] = "yellow"
      box.select()
    elif box["bg"] == "yellow":
      box["bg"] = self.bg
      self.checked_boxes.remove(cat)

  def _layoutItemEditorArea(self):
    """Internal method _configureColsRows the skill editor panel."""
  
    # Clear previous widgets to prevent overlap and general yuck
    for widget in self.skill_editor_area.grid_slaves():
      widget.grid_forget()
    item_name = self.item[0] if self.item else "Nothing? Whu? How?"
    if self.item_type == "skills":
      label = item_name + " -- Page(s): " + self.item[-2]
    else:
      label = item_name + " -- Page(s): " + self.item[-3]
    tk.Label(self.skill_editor_area,
             text = label,
             bg = self.bg).grid(row = self.skill_editor_area.grid_size()[1],
                                columnspan = 3,
                                pady = 25)
    self.submit_skill_button.grid(row = self.skill_editor_area.grid_size()[1],
                                  sticky = tk.N + tk.W + tk.E,
                                  columnspan = 3,
                                  pady = 15)
    tk.Label(self.skill_editor_area,
             text = "Skill Categories",
             bg = self.bg).grid(row = self.skill_editor_area.grid_size()[1],
                                column = 0,
                                columnspan = 3)
    row = self.skill_editor_area.grid_size()[1] - 1
    for idx, category in enumerate(sorted(self.item_categories)):
      bgyeller = False
      if category not in self.checkboxes.keys():
        self.checkboxes[category] = {}
        self.checkboxes[category]["var"] = tk.IntVar()
        self.checkboxes[category]["checkbox"] = tk.Checkbutton(self.skill_editor_area,
                                                                text = category,
                                                                variable = self.checkboxes[category]["var"],
                                                                command = self.doubleCheck,
                                                                bg = self.bg)
      col = idx % 3
      if col == 0:
        row += 1
      self.checkboxes[category]["checkbox"].grid(row = row,
                                                 column = col,
                                                 sticky = tk.W)
      if self.item:
        this_item = [i for i in self.item[-1] if category in i]
        if this_item:
          self.checkboxes[category]["var"].set(1)
          if "---" in this_item[0]:
            self.checkboxes[category]["checkbox"]["bg"] = "yellow"
            self.checkboxes[category]["checkbox"]["text"] = category.replace("---","")
          self.checked_boxes.append(category)
        else:
          self.checkboxes[category]["var"].set(0)
    current_row = self.skill_editor_area.grid_size()[1]
    tk.Label(self.skill_editor_area,
             text = "Min TL",
             bg = self.bg).grid(row = current_row)
    if self.item_type == "skills":
      tl_index = 3
    else:
      tl_index = 5
    self.tech_level_spinbox.grid(row = current_row,
                                 column = 1,
                                 columnspan = 2,
                                 sticky = tk.N + tk.W + tk.E,
                                 pady = 5)
    self.tech_level_spinbox.delete(0, "end")
    self.tech_level_spinbox.insert(0, self.item[tl_index][0])
    current_row = self.skill_editor_area.grid_size()[1]
    tk.Label(self.skill_editor_area,
             text = "Max TL",
             bg = self.bg).grid(row = current_row)
    self.max_tech_level_spinbox.grid(row = current_row,
                                     column = 1,
                                     columnspan = 2,
                                     sticky = tk.N + tk.W + tk.E,
                                     pady = 5)
    self.max_tech_level_spinbox.delete(0, "end")
    self.max_tech_level_spinbox.insert(0, self.item[tl_index][1])
    if self.item_type == "skills":
      self.skill_prereq_label.grid(row = self.skill_editor_area.grid_size()[1],
                                   columnspan = 3)
      self.skill_prereq_entry.grid(row = self.skill_editor_area.grid_size()[1],
                                   columnspan = 3,
                                   sticky = tk.W + tk.E)
      self.cancel_skill_button.grid(row = self.skill_editor_area.grid_size()[1],
                                    sticky = tk.N + tk.W + tk.E,
                                    columnspan = 3,
                                    pady = 30)

  def _gridWidgets(self):

    Y = 5
    # Grid areas
    self.listbox_area.grid(row=0,
                           column=0,
                           sticky=tk.N+tk.S+tk.W+tk.E)
    self.searchbar_area.grid(row=0,
                             column=0,
                             pady=Y,
                             sticky=tk.NW)
    self.button_area.grid(row=0,
                          column=1,
                          sticky=tk.N+tk.S,
                          pady=10)

    # listbox widgets
    self.previous_button.grid(row=0,
                          column=1,
                          pady=Y,
                          sticky=tk.NE)
    self.searchbar_entry.grid(row=0,
                              column=1,
                              padx=5)
    self.searchbar_button.grid(row=0,
                               column = 0,
                               padx = 5)
    self.next_button.grid(row = 0,
                          column = 2,
                          pady = Y,
                          sticky = tk.NE)

    self.activateSkillList()
    self.tab_area.grid(row = 2,
                       column = 0,
                       sticky = tk.W,
                       padx = 5)
    self.skill_tab.grid(row = 0,
                        column = 0,
                        sticky = tk.W,
                        padx = 3)
    self.advantages_tab.grid(row = 0,
                             column = 1,
                             sticky = tk.W,
                             padx = 3)
    self.disadvantages_tab.grid(row = 0,
                                column = 2,
                                sticky = tk.W,
                                padx = 3)

    # Action button widgets
    self.select_skill_button.grid(row = 1,
                                  column = 0,
                                  pady = Y,
                                  sticky = tk.E + tk.W + tk.N)
    self.new_category_button.grid(row = self.button_area.grid_size()[1],
                                  pady = Y,
                                  sticky = tk.N + tk.W + tk.E)
    self.refresh_button.grid(row = self.button_area.grid_size()[1],
                             pady = Y,
                             sticky = tk.N + tk.W + tk.E)
    self.quit_button.grid(row = self.button_area.grid_size()[1],
                          column = 0,
                          pady = Y,
                          sticky = tk.E + tk.W + tk.N)
    # Stats label
    self.stats_label.grid(row = self.grid_size()[1] - 1,
                          column = self.grid_size()[0] - 1,
                          pady = Y,
                          sticky = tk.S + tk.W)

    # Configure specific frames
    self.listbox_area.rowconfigure(1, weight=1)
    self.listbox_area.columnconfigure(0, weight=1)

  def _createWidgets(self):
    
    self.listbox_area = tk.Frame(self, bg = self.bg)
    self.skill_editor_area = tk.Frame(self, bg = self.bg)
    self.category_editor_area = tk.Frame(self, bg = self.bg)
    self.button_area = tk.Frame(self, bg = self.bg)
    self.searchbar_area = tk.Frame(self.listbox_area, bg = self.bg)
    self.tab_area = tk.Frame(self.listbox_area, bg = self.bg)

    self.searchbar_stringvar = tk.StringVar()
    self.searchbar_entry = tk.Entry(self.searchbar_area,
                                    textvariable = self.searchbar_stringvar,
                                    width = 35)
    self.searchbar_entry.bind("<Return>", self.searchActiveList)
    self.searchbar_button = tk.Button(self.searchbar_area,
                                      width = 7,
                                      text = "Search",
                                      command = self.searchActiveList)
    self.next_button = tk.Button(self.listbox_area,
                                 text = "v Next v",
                                 command = self.nextSkill,
                                 width = 12)
    self.previous_button = tk.Button(self.listbox_area,
                                 text = "^ Previous ^",
                                 command = self.previousSkill,
                                 width = 12)
    # Skill listbox
    self.skill_list_scrollbar = tk.Scrollbar(self.listbox_area,
                                             bg = self.bg)
    self.skill_list_listbox = tk.Listbox(self.listbox_area,
                                         border = 3,
                                         bg = self.bg,
                                         yscrollcommand = self.skill_list_scrollbar.set)
    self.skill_list_listbox.bind("<Double-Button-1>", self.selectItem)
    self.skill_list_scrollbar.config(command = self.skill_list_listbox.yview)
    # Advantages listbox
    self.advantages_list_scrollbar = tk.Scrollbar(self.listbox_area,
                                             bg = self.bg)
    self.advantages_list_listbox = tk.Listbox(self.listbox_area,
                                         border = 3,
                                         bg = self.bg,
                                         yscrollcommand = self.advantages_list_scrollbar.set)
    self.advantages_list_listbox.bind("<Double-Button-1>", self.selectItem)
    self.advantages_list_scrollbar.config(command = self.advantages_list_listbox.yview)
    # Disadvantages listbox
    self.disadvantages_list_scrollbar = tk.Scrollbar(self.listbox_area,
                                             bg = self.bg)
    self.disadvantages_list_listbox = tk.Listbox(self.listbox_area,
                                         border = 3,
                                         bg = self.bg,
                                         yscrollcommand = self.disadvantages_list_scrollbar.set)
    self.disadvantages_list_listbox.bind("<Double-Button-1>", self.selectItem)
    self.disadvantages_list_scrollbar.config(command = self.disadvantages_list_listbox.yview)
    # Tab buttons to change lists
    self.skill_tab = tk.Button(self.tab_area,
                               text = "Skills",
                               width = 15,
                               command = self.activateSkillList)
    self.advantages_tab = tk.Button(self.tab_area,
                                    text = "Advantages",
                                    width = 15,
                                    command = self.activateAdvantagesList)
    self.disadvantages_tab = tk.Button(self.tab_area,
                                       text = "Disadvantages",
                                       width = 15,
                                       command = self.activateDisadvantagesList)
    self.stats_label = tk.Label(self,
                                textvariable = self.stats,
                                bg = self.bg)
    self.select_skill_button = tk.Button(self.button_area,
                                         text = "Edit Selected",
                                         command = self.selectItem)
    self.new_category_button = tk.Button(self.button_area,
                                         text = "New Category",
                                         command = self._newCategory)
    self.refresh_button = tk.Button(self.button_area,
                                    text = "Refresh",
                                    command = self.updateData)
    self.quit_button = tk.Button(self.button_area,
                                 text = "Quit",
                                 command = self.quit)
    self.submit_skill_button = tk.Button(self.skill_editor_area,
                                   text = "Submit",
                                   command = self._saveItem)
    self.tech_level_spinbox = tk.Spinbox(self.skill_editor_area,
                                         from_ = 0,
                                         to_ = 13)
    self.max_tech_level_spinbox = tk.Spinbox(self.skill_editor_area,
                                         from_ = 0,
                                         to_ = 13)
    self.skill_prereq_label = tk.Label(self.skill_editor_area,
                                       text = "Prerequisites (comma delimited)",
                                       bg = self.bg)
    self.skill_prereq_entry_var = tk.StringVar()
    self.skill_prereq_entry = tk.Entry(self.skill_editor_area,
                                       textvariable = self.skill_prereq_entry_var,
                                       width = 40)
    self.cancel_skill_button = tk.Button(self.skill_editor_area,
                                         text="Cancel",
                                         command=self._cancelItem)
    tk.Label(self.category_editor_area,
             text = "Enter a new category",
             bg = self.bg).grid(row = 0,
                              column = 0,
                              columnspan = 2)
    self.category_entry_var = tk.StringVar()
    self.category_entry = tk.Entry(self.category_editor_area,
                                   textvariable = self.category_entry_var,
                                   width = 40)
    self.category_submit_button = tk.Button(self.category_editor_area,
                                            text = "Submit",
                                            command = self._saveCategory)
    self.category_cancel_button = tk.Button(self.category_editor_area,
                                           text="Cancel",
                                           command = self.cancel_newCategory)

  def saveData(self):
    with open(gdats[self.item_type], "w") as f:
      f.writelines(data[self.item_type])

  def updateData(self):

    self.item_categories = set([])
    self.skill_list = []
    self.advantages_list = []
    self.disadvantages_list = []
    # Eval skills
    for line in data["skills"]:
      skill = eval(line)
      self.skill_list.append(skill)
      for cat in skill[-1]:
        self.item_categories.add(cat.strip("---"))
    # Eval advantages
    for line in data["advantages"]:
      advantage = eval(line)
      self.advantages_list.append(advantage)
      for cat in advantage[-1]:
        self.item_categories.add(cat.strip("---"))
    # Eval disadvantages
    for line in data["disadvantages"]:
      disadvantage = eval(line)
      self.disadvantages_list.append(disadvantage)

  def _run(self):

    self.updateData()
    self.grid()
    self._createWidgets()
    self._gridWidgets()
    self._populateSkillList()
    self._populateAdvantagesList()
    self._populateDisadvantagesList()
    self._configureColsRows()


if __name__ == "__main__":
  app = Application("#999")
  app.master.title("GURPS CG Trait Editor")
  app.master.geometry("1050x800+200+200")
  app.mainloop()
