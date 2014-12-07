__author__ = 'open64'
from ttk import *
from tkinter import *
import os
from FileManager.tabs.work_space.work_space import WorkSpace
import sys


class Tabs(Notebook):
    def __init__(self, parent):
        self.__window = parent
        Notebook.__init__(self, parent)
        self.__style = Style(self)
        self.__set_style()
        self.__arr_tabs = list()
        self.add_tab(os.getcwd())
        self.__create_menu()
        self.__bind_tab()

    def add_tab(self, path=None):
        if path:
            self.__arr_tabs.append(WorkSpace(self.__window, self, path))
        else:
            self.__arr_tabs.append(WorkSpace(self.__window, self, self.curr_tab().get_path()))
        self.__arr_tabs[-1].pack()
        self.__arr_tabs[-1].bind('<BackSpace>', lambda event: self.__window.get_tools_panel().change_address())
        self.add(self.__arr_tabs[-1], text=self.__arr_tabs[-1].get_curr_dir())

    def rem_tab(self):
        idx = self.idx_curr_tab()
        self.__arr_tabs[idx].destroy()
        self.__arr_tabs.pop(idx)
        if not self.__arr_tabs:
            sys.exit(0)

    def idx_curr_tab(self):
        return self.index(self.select())

    def curr_tab(self):
        return self.__arr_tabs[self.idx_curr_tab()]

    def set_curr_tab(self, idx):
        self.select(idx)

    def rename_tab(self, new_dir, open_dir, change_address):
        idx = self.idx_curr_tab()
        if new_dir == os.path.sep:
            self.tab(idx, text=new_dir)
        else:
            self.tab(idx, text=os.path.basename(new_dir))
        if open_dir:
            self.curr_tab().open_directory(new_dir, rename_tab=False)
        if change_address:
            self.__window.get_tools_panel().change_address(new_address=new_dir, rename_tab=False)

    def __change_tab(self):
        path = self.curr_tab().get_path()
        os.chdir(path)
        self.__window.get_tools_panel().change_address(new_address=path, rename_tab=False)

    def __bind_tab(self):
        self.bind('<Button-2>', lambda e: self.rem_tab())
        self.bind('<Button-3>', self.__call_context_menu)
        self.bind('<<NotebookTabChanged>>', lambda e: self.__change_tab())
        self.__menu.bind('<FocusOut>', lambda e: self.__menu.unpost())

    def __call_context_menu(self, event):
        self.__menu.post(event.x_root, event.y_root)
        self.__menu.focus()

    def __create_menu(self):
        self.__menu = Menu(self, tearoff=False)
        self.__menu.add_command(label='New Tab', command=self.add_tab, underline=0)
        self.__menu.add_command(label='Remove Tab', command=self.rem_tab, underline=0)

    def __set_style(self):
        style_name = 'blue-dark-theme'
        self.__style.theme_create(
            style_name, parent="alt", settings={
                "TNotebook": {
                    "configure": {
                        "tabmargins": [2, 4, 2, 0]
                    }
                },
                "TNotebook.Tab": {
                    "configure": {
                        "padding": [5, 2],
                        "background": '#2644A2',
                        'font': 'helvetica',
                        'foreground': "white"
                    },
                    "map": {
                        "background": [("selected", '#1B2B5C')],
                        "expand": [("selected", [1, 1, 1, 0])]
                    }
                }
            }
        )
        self.__style.theme_use(style_name)
