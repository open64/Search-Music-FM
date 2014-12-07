__author__ = 'open64'

from tkinter import messagebox
from tkinter import *
from FileManager.tools_panel.tools_button import ToolsButton
import os


class Tools(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.__window = parent
        self.config(bg='#5E6275')
        self.__address = Entry(self)
        self.__address.insert(0, os.getcwd())
        self.__address.pack(fill=X, side=LEFT, expand=YES)
        self.__bind_tools()
        ToolsButton(self, text='Up', command=self.change_address).pack(side=RIGHT)
        ToolsButton(
            self,
            text='Go', command=lambda: self.change_address(new_address=self.__address.get())
        ).pack(side=RIGHT)

    def focus(self):
        self.__address.focus()

    def change_address(self, **kw):
        new_address = kw.get('new_address')
        if not new_address:
            address = self.__address.get()
            new_address = address[:address.rfind(os.path.sep)]
            if new_address == '':
                new_address = os.path.sep
        if os.path.isdir(new_address):
            if new_address[-1] == os.path.sep and len(new_address) > 1:
                new_address = new_address[:-1]
            self.__address.delete(0, END)
            self.__address.insert(0, new_address)
            if kw.get('rename_tab', True):
                self.__get_tabs().rename_tab(new_address, True, False)
        else:
            wrong_address = 'You enter wrong address!\nDirectory "' + new_address + '" is not exist.'
            messagebox.showerror('Wrong address', wrong_address)

    def __get_tabs(self):
        return self.__window.get_tabs()

    def __bind_tools(self):
        self.__address.bind('<Return>', lambda event: self.change_address(new_address=self.__address.get()))
