__author__ = 'open64'

from tkinter import *
from FileManager.menu import MenuFM
from FileManager.tools_panel.tools import Tools
from FileManager.navigation_panel.navigation import Navigation
from FileManager.tabs.tabs import Tabs


class FileManager(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title('File Manager')
        self.geometry('850x600')
        self.__make_widgets()
        self.__bind_window()

    def __make_widgets(self):
        self.__navigation = Navigation(self)
        self.__tabs = Tabs(self)
        self.__tools_panel = Tools(self)
        self.__tools_panel.pack(side=TOP, fill=BOTH)
        self.__navigation.pack(side=LEFT, fill=BOTH)
        self.__tabs.pack(side=RIGHT, expand=YES, fill=BOTH)
        self.__menu = MenuFM(self)

    def __bind_window(self):
        self.__focus_f6 = self.__tools_panel
        self.__change_focus()
        self.bind('<F6>', self.__change_focus)
        self.bind('<Control-t>', lambda event: self.__tabs.add_tab())
        self.bind('<Control-w>', lambda event: self.__tabs.rem_tab())
        for i in range(9):
            self.bind('<Alt-Key-%d>' % (i+1), lambda event, idx=i: self.__tabs.set_curr_tab(idx))
        self.bind('<Alt-Key-0>', lambda event: self.__tabs.set_curr_tab(9))

    def __change_focus(self, event=None):
        if self.__focus_f6 == self.__tools_panel:
            self.__focus_f6 = self.__tabs.curr_tab()
        else:
            self.__focus_f6 = self.__tools_panel
        self.__focus_f6.focus()

    def get_tools_panel(self):
        return self.__tools_panel

    def get_tabs(self):
        return self.__tabs

if __name__ == '__main__':
    FileManager().mainloop()
