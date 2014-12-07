__author__ = 'open64'
from tkinter import *
from tkinter.messagebox import *


class MenuFM(Menu):
    def __init__(self, window):
        self.__window = window
        Menu.__init__(self, self.__window)
        self.__window.config(menu=self)
        self.config(bg='#3A3F4E', fg='white')
        self.make_file()
        self.make_edit()
        self.make_view()
        self.make_service()
        self.make_bookmarks()
        self.make_help()

    def make_file(self):
        file = Menu(self)
        file.add_command(label='New Window', command=None, underline=4)
        file.add_command(label='New Tab', command=self.__window.get_tabs().add_tab, underline=4)
        file.add_command(label='Open', command=self.__open_file, underline=0)
        file.add_command(label='Open in New Tab', command=lambda: self.__open_file(new_tab=True), underline=12)
        file.add_command(label='Open in New Window', command=self.quit, underline=12)
        file.add_command(label='Quit', command=self.quit, underline=0)
        self.add_cascade(label='File', menu=file, underline=0)

    def make_edit(self):
        edit = Menu(self)
        edit.add_command(label='Undo', command=self.quit, underline=0)
        edit.add_command(label='Redo', command=self.quit, underline=0)
        edit.add_command(label='Cut', command=self.quit, underline=0)
        edit.add_command(label='Copy', command=self.quit, underline=1)
        edit.add_command(label='Paste', command=self.quit, underline=0)
        edit.add_command(label='Select all', command=self.quit, underline=0)
        edit.add_command(label='Select item matching...', command=self.quit, underline=7)
        edit.add_command(label='Invert select', command=self.quit, underline=0)
        edit.add_command(label='Make link', command=self.quit, underline=5)
        edit.add_command(label='Rename', command=self.quit, underline=2)
        edit.add_command(label='Move to Trash', command=self.quit, underline=0)
        self.add_cascade(label='Edit', menu=edit, underline=0)

    def make_view(self):
        view = Menu(self)
        self.add_cascade(label='View', menu=view, underline=0)

    def make_bookmarks(self):
        bookmarks = Menu(self)
        self.add_cascade(label='Bookmarks', menu=bookmarks, underline=0)

    def make_service(self):
        service = Menu(self)
        self.add_cascade(label='Service', menu=service, underline=0)

    def make_help(self):
        help_ = Menu(self)
        help_.add_command(label='About', command=MenuFM.__call_about, underline=0)
        self.add_cascade(label='Help', menu=help_, underline=0)

    @staticmethod
    def __call_about():
        showinfo('About', 'Search Music FM v0.1.2')

    def __open_file(self, **kw):
        tab = self.__window.get_tabs().curr_tab()
        select_file = tab.get_select_file()
        if select_file is not None:
            tab.get_file(select_file).open(kw)