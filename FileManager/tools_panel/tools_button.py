__author__ = 'open64'
from tkinter import *


class ToolsButton(Button):
    def __init__(self, parent=None, cnf=None, **kw):
        if not cnf:
            cnf = dict()
        Button.__init__(self, parent, cnf, **kw)
        self.config(relief=RAISED, bd=2)
        self.config(font=('Courier', 10, 'bold'))
        self.config(bg='#6A6868', fg='white')