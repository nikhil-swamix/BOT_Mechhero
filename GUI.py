from tkinter import *

class BasicGUI:
   '''docstring'''
   def __init__(self,arg):
      self.window = Tk()
      self.window.title("Welcome to LikeGeeks app")
      self.lbl = Label(window, text="Hello")
      lbl.grid(column=0, row=0)

   def render(self):
      self.window.mainloop()



