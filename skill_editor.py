'''
Created on Oct 25, 2013

@author: Justin
'''

import Tkinter as tk
import tkMessageBox as tkmsg
import re


with open("C:\\Users\\Justin\\Projects\\gurpscg\\gurpscg\\traits\\skills.dat", "r") as file:
  DATA = file.readlines()


class Application(tk.Frame):
  
  def __init__(self, bg_color, master=None):
    tk.Frame.__init__(self, master,
                      bg=bg_color)

    # Allow for window resizing
    top=self.winfo_toplevel()                
    top.rowconfigure(0, weight=1)
    top.columnconfigure(0, weight=1)         
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    self.grid(sticky=tk.N+tk.S+tk.E+tk.W)

    self.bg = bg_color
    self.checkboxes = {}
    self.skill = None
    self.skill_index = None
    self.stats = tk.StringVar()
    self.run()

  def populateSkillList(self):
    
    self.incomplete_count = 0
    self.skill_list_listbox.delete(0, tk.END)
    self.skill_list_listbox.delete(0, tk.END)
    for i in sorted(self.skill_list):
      if i[-1]:
        name = i[0]
      else:
        name = i[0] + " ... Incomplete!"
        self.incomplete_count += 1
      self.skill_list_listbox.insert(tk.END, name)
    self.updateStatsWidget()

  def updateStatsWidget(self):
    
    stats = "Skills: %(skill_count)s\nUnconfigured: %(incomplete_count)s" %(
        self.__dict__)
    percent = 100 - int((float(self.incomplete_count) / self.skill_count) * 100) 
    stats += "\nWinning: %s%%" % percent
    self.stats.set(stats)

  def configureColsRows(self):
    
    col, row = self.grid_size()
    for i in range(col):
      self.grid_columnconfigure(i, pad=20,)
    for i in range(row):
      self.grid_rowconfigure(i, pad=20,)

  def newCategory(self):
    
    self.category_editor_area.grid(column=self.grid_size()[0],
                                   row=0)
    self.category_entry.grid(row=1,
                             columnspan=2,
                             pady=10,
                             sticky=tk.W+tk.E)
    self.category_submit_button.grid(row=2,
                                     column=0,
                                     padx=5,
                                     sticky=tk.E+tk.W)
    self.category_cancel_button.grid(row=2,
                                    column=1,
                                    padx=5,
                                    sticky=tk.E+tk.W)
    self.configureColsRows()

  def saveCategory(self):
    
    new_cat = self.category_entry_var.get().split()
    if new_cat:
      new_cat = " ".join([i[0].upper() + i[1:].lower() for i in new_cat])
      self.skill_categories.add(new_cat)
      self.cancelNewCategory()
      self._layoutSkillEditorArea()
    else:
      tkmsg.showerror(
          "Type Somethin'", "Sorry, Boss. We can't have nil cats runnin'round!")

  def cancelNewCategory(self):
    
    self.category_editor_area.grid_forget()

  def selectSkill(self, event=None):
    
    if event:
      widget = event.widget
      selection=widget.curselection()
      raw_name = widget.get(selection[0])
    else:
      raw_name = self.skill_list_listbox.get(tk.ACTIVE)
    skill_name = raw_name.split(" ... ")[0].strip()
    self.listbox_position = self.skill_list_listbox.get(0,tk.END).index(raw_name)
    for i in self.skill_list:
      if i[0] == skill_name:
        self.skill = i
    for i in DATA:
      if eval(i)[0] == skill_name:
        self.skill_index = DATA.index(i)
        if type(self.skill[-3]) == type([]):
          self.skill_prereq_entry_var.set(", ".join(self.skill[-3]))
        else:
          self.skill_prereq_entry_var.set("")
    if self.skill_index != None:
      self.skill_editor_area.grid(row=0,
                                  column=self.grid_size()[0],
                                  sticky=tk.W+tk.E+tk.N+tk.S)
    else:
      self.skill = None
    self._layoutSkillEditorArea()
    self.configureColsRows()

  def saveSkill(self):

    kitties = []
    for cat,check in self.checkboxes.items():
      if check.get() == 1:
        kitties.append(cat)
    self.skill[3] = int(self.tech_level_spinbox.get())
    self.skill[-1] = kitties
    prereqs = self.skill_prereq_entry_var.get().split(", ")
    if prereqs[0] == '':
      prereqs = []
    if len(self.skill) == 6:
      self.skill.insert(-2, prereqs)
    elif len(self.skill) == 7:
      self.skill[-3] = prereqs
    else:
      print self.skill
    DATA[self.skill_index] = str(self.skill) + "\n"
    self.cancelSkill()
    self.saveData()
    self.updateData()
    self.populateSkillList()
    self.skill_list_listbox.see(self.listbox_position + 10)
    self.skill_list_listbox.activate(self.listbox_position + 1)


  def cancelSkill(self):

    self.skill = None
    self.skill_index = None
    self.skill_editor_area.grid_forget()
  
  def nextSkill(self):
    
    active = self.skill_list_listbox.get(tk.ACTIVE)
    listbox_contents = self.skill_list_listbox.get(0,tk.END)
    current_pos = listbox_contents.index(active)
    if current_pos + 1 >= 0:
      new_pos = current_pos + 1
      self.skill_list_listbox.activate(new_pos)
      self.skill_list_listbox.select_clear(current_pos)
      self.skill_list_listbox.selection_set(tk.ACTIVE)
  
  def previousSkill(self):
    
    active = self.skill_list_listbox.get(tk.ACTIVE)
    listbox_contents = self.skill_list_listbox.get(0,tk.END)
    current_pos = listbox_contents.index(active)
    if current_pos + 1 >= 0:
      new_pos = current_pos - 1
      self.skill_list_listbox.activate(new_pos)
      self.skill_list_listbox.select_clear(current_pos)
      self.skill_list_listbox.selection_set(tk.ACTIVE)

  def searchActiveList(self):
    
    print "search!"

  def _layoutSkillEditorArea(self):
    """Internal method configureColsRows the skill editor panel."""
  
    for widget in self.skill_editor_area.grid_slaves():
      widget.grid_forget()
    skill_name = self.skill[0] if self.skill else "Nothing? Whu? How?"
    label = skill_name + " -- Page(s): " + self.skill[-2]
    tk.Label(self.skill_editor_area,
             text=label,
             bg=self.bg).grid(row=self.skill_editor_area.grid_size()[1],
                                   columnspan=3,
                                   pady=25)
    self.submit_skill_button.grid(row=self.skill_editor_area.grid_size()[1],
                                  sticky=tk.N+tk.W+tk.E,
                                  columnspan=3,
                                  pady=15)
    tk.Label(self.skill_editor_area,
             text="Skill Categories",
             bg=self.bg).grid(row=self.skill_editor_area.grid_size()[1],
                                           column=0,
                                           columnspan=3)
    self.checkboxes = {}
    row = self.skill_editor_area.grid_size()[1] - 1
    for idx,category in enumerate(sorted(self.skill_categories)):
      col = idx % 3
      if col == 0:
        row += 1
      self.checkboxes[category] = tk.IntVar()
      tk.Checkbutton(self.skill_editor_area,
                     text=category,
                     variable=self.checkboxes[category],
                     bg=self.bg).grid(row=row,
                                                 column=col,
                                                 sticky=tk.W)
      if self.skill and category in self.skill[-1]:
        self.checkboxes[category].set(1)
      else:
        self.checkboxes[category].set(0)

    self.tech_level_spinbox.grid(row=self.skill_editor_area.grid_size()[1],
                                                      columnspan=3,
                                                      sticky=tk.N+tk.W+tk.E,
                                                      pady=5)
    self.tech_level_spinbox.delete(0, "end")
    self.tech_level_spinbox.insert(0, self.skill[3])
    self.skill_prereq_label.grid(row=self.skill_editor_area.grid_size()[1],
                                 columnspan=3)
    self.skill_prereq_entry.grid(row=self.skill_editor_area.grid_size()[1],
                                 columnspan=3,
                                 sticky=tk.W+tk.E)
    self.cancel_skill_button.grid(row=self.skill_editor_area.grid_size()[1],
                                  sticky=tk.N+tk.W+tk.E,
                                  columnspan=3,
                                  pady=30)

  def gridWidgets(self):

    Y = 5
    self.searchbar_area.grid(row=0,
                             column=1,
                             pady=Y,
                             sticky=tk.N+tk.S+tk.W)
    self.searchbar_entry.grid(row=0,
                              column=0,
                              pady=Y,
                              padx=2)
    self.searchbar_button.grid(row=0,
                               column=1,
                               pady=Y,
                               padx=2)
    self.listbox_area.grid(row=0,
                           column=0,
                           sticky=tk.N+tk.S+tk.W+tk.E)
    self.next_button.grid(row=0,
                          column=2,
                          pady=Y,
                          sticky=tk.E)
    self.previous_button.grid(row=0,
                          column=0,
                          pady=Y,
                          sticky=tk.W)
    self.skill_list_listbox.grid(row=1,
                                 column=0,
                                 columnspan=2,
                                 sticky=tk.N+tk.S+tk.W+tk.E)
    self.skill_list_scrollbar.grid(row=1,
                                   column=2,
                                   sticky=tk.N+tk.S+tk.W)
    self.button_area.grid(row=0,
                          column=1,
                          sticky=tk.N+tk.S,
                          pady=10)
    self.select_skill_button.grid(row=1,
                                  column=0,
                                  pady=Y,
                                  sticky=tk.E+tk.W+tk.N)
    self.new_category_button.grid(row=self.button_area.grid_size()[1],
                                  pady=Y,
                                  sticky=tk.N+tk.W+tk.E)
    self.refresh_button.grid(row=self.button_area.grid_size()[1],
                             pady=Y,
                             sticky=tk.N+tk.W+tk.E)
    self.quit_button.grid(row=self.button_area.grid_size()[1],
                          column=0,
                          pady=Y,
                          sticky=tk.E+tk.W+tk.N)
    self.stats_label.grid(row=self.grid_size()[1] -1,
                          column=self.grid_size()[0] -1,
                          pady=Y,
                          sticky=tk.S+tk.W)

  def createWidgets(self):
    
    self.listbox_area = tk.Frame(self, bg=self.bg)
    self.listbox_area.columnconfigure(0, weight=1)
    self.listbox_area.rowconfigure(1, weight=1)
    self.skill_editor_area = tk.Frame(self, bg=self.bg)
    self.category_editor_area = tk.Frame(self, bg=self.bg)
    self.button_area = tk.Frame(self, bg=self.bg)
    self.searchbar_area = tk.Frame(self.listbox_area, bg=self.bg)

    self.searchbar_stringvar = tk.StringVar()
    self.searchbar_entry = tk.Entry(self.searchbar_area,
                                    textvariable=self.searchbar_stringvar,
                                    width=35)
    self.searchbar_button = tk.Button(self.searchbar_area,
                                      width=7,
                                      text="Search",
                                      command=self.searchActiveList)
    self.next_button = tk.Button(self.listbox_area,
                                 text="v Next v",
                                 command=self.nextSkill,
                                 width=12)
    self.previous_button = tk.Button(self.listbox_area,
                                 text="^ Previous ^",
                                 command=self.previousSkill,
                                 width=12)
    self.skill_list_scrollbar = tk.Scrollbar(self.listbox_area,
                                             bg=self.bg) 
    self.skill_list_listbox = tk.Listbox(self.listbox_area,
                                         border=3,
                                         bg=self.bg,
                                         yscrollcommand=self.skill_list_scrollbar.set)
    self.skill_list_listbox.bind("<Double-Button-1>", self.selectSkill)
    self.skill_list_scrollbar.config(command=self.skill_list_listbox.yview)
    self.stats_label = tk.Label(self,
                                textvariable=self.stats,
                                bg=self.bg)
    self.select_skill_button = tk.Button(self.button_area,
                                         text="Edit Selected",
                                         command=self.selectSkill)
    self.new_category_button = tk.Button(self.button_area,
                                         text="New Category",
                                         command=self.newCategory)
    self.refresh_button = tk.Button(self.button_area,
                                    text="Refresh",
                                    command=self.updateData)
    self.quit_button = tk.Button(self.button_area,
                                 text="Quit",
                                 command=self.quit)
    self.submit_skill_button = tk.Button(self.skill_editor_area,
                                   text="Submit",
                                   command=self.saveSkill)
    self.tech_level_spinbox = tk.Spinbox(self.skill_editor_area,
                                         from_=0,
                                         to_=13)
    self.skill_prereq_label = tk.Label(self.skill_editor_area,
                                       text="Prerequisites (comma delimited)",
                                       bg=self.bg)
    self.skill_prereq_entry_var = tk.StringVar()
    self.skill_prereq_entry = tk.Entry(self.skill_editor_area,
                                       textvariable=self.skill_prereq_entry_var,
                                       width=40)
    self.cancel_skill_button = tk.Button(self.skill_editor_area,
                                         text="Cancel",
                                         command=self.cancelSkill)
    tk.Label(self.category_editor_area,
             text="Enter a new category",
             bg=self.bg).grid(row=0,
                              column=0,
                              columnspan=2)
    self.category_entry_var = tk.StringVar() 
    self.category_entry = tk.Entry(self.category_editor_area,
                                   textvariable=self.category_entry_var,
                                   width=40)
    self.category_submit_button = tk.Button(self.category_editor_area,
                                            text="Submit",
                                            command=self.saveCategory)
    self.category_cancel_button = tk.Button(self.category_editor_area,
                                           text="Cancel",
                                           command=self.cancelNewCategory)

  def saveData(self):
    with open("C:\\Users\\Justin\\Projects\\gurpscg\\gurpscg\\traits\\skills.dat", "w") as file:
      file.writelines(DATA)

  def updateData(self):
    
    self.skill_count = 0
    self.skill_categories = set([])
    self.skill_list = []
    for line in DATA:
      skill = eval(line)
      self.skill_count += 1
      self.skill_list.append(skill)
      for cat in skill[-1]:
        self.skill_categories.add(cat)

  def run(self):
    
    self.updateData()
    self.grid()
    self.createWidgets()
    self.populateSkillList()
    self.gridWidgets()
    self.configureColsRows()
    

if __name__ == "__main__":
  app = Application("#999")
  app.master.title("Skill Editor")
  app.master.geometry("700x600+200+200")
  app.mainloop()
