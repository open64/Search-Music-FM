__author__ = 'open64'
from tkinter import *
from PIL import Image
import os
import sys


class File(Frame):
    IMAGE_PATH = os.path.join(sys.path[0], 'image') + os.path.sep

    def __init__(self, file_name, dir_name, parent, **kw):
        self._work_space = parent
        Frame.__init__(self, self._work_space.get_canvas())
        self.__default_style = kw
        self.__focus_style = dict(bg='#7C7CAF')

        self.__canvas = Canvas(self, takefocus=1)
        self._name = Label(self, takefocus=1)
        self.__name_entry = Entry(self)
        self.__name_entry.insert(0, file_name)
        self._icon = PhotoImage()
        self.set_default_icon()
        self._dir = dir_name

        self.__set_name(file_name)
        self.__configure_canvas()
        self.config(
            width=self._name.winfo_reqwidth() + self.__canvas.winfo_reqwidth(),
            height=self.__canvas.winfo_reqheight()
        )
        self._file_focus_out()
        self.__bind_file()

    def set_icon(self, image=None):
        if image:
            self._icon.config(file=image)
            self._resize_canvas()

    def set_default_icon(self):
        self._icon.config(file=self._get_default_image())
        self._resize_canvas()

    def _get_default_image(self):
        pass

    def open(self, **kw):
        pass

    def set_id(self, id_file):
        self.__id = id_file

    def get_name(self):
        return self._name.cget('text')

    def focus(self):
        self._name.focus_set()

    def rename(self):
        new_name = self.__name_entry.get()
        os.rename(self._name.cget('text'), new_name)
        self.__set_name(new_name)
        self._name.focus()

    def remove(self):
        self._work_space.open_directory(self._dir)
        self._work_space.set_focus_file()

    def cut(self):
        self._work_space.set_buffer(os.path.join(self._dir, self._name.cget('text')), 'cut')

    def copy(self):
        self._work_space.set_buffer(os.path.join(self._dir, self._name.cget('text')), 'copy')

    def make_link(self):
        source = os.path.join(self._dir, self._name.cget('text'))
        os.symlink(source, 'link ' + self._name.cget('text'))
        self._work_space.open_directory(self._dir)

    def property(self):
        pass

    def cancel_rename(self):
        self.__name_entry.delete(0, END)
        self.__name_entry.insert(0, self._name.cget('text'))
        self.__set_name()
        self._name.focus()

    def start_renaming(self):
        if self._work_space.get_focus_file() == self.__id and self._work_space.get_select_file() == self.__id:
            self._name.pack_forget()
            self.__name_entry.pack()
            self.__name_entry.focus()
        else:
            self._name.focus()

    def _resize_canvas(self):
        self.__canvas.config(width=self._icon.width(), height=self._icon.height())

    def _change_file_focus(self, move):
        self._work_space.select_focus_file(move)

    def _file_focus_in(self):
        self._name.config(self.__focus_style)
        self.__canvas.config(self.__focus_style)
        self._work_space.set_focus_file(self.__id)
        self._work_space.set_select_file(self.__id)

    def _file_focus_out(self):
        self._name.config(self.__default_style)
        self.__canvas.config(self.__default_style)

    def _context_menu(self, event):
        self._file_focus_in()
        menu = File.__create_context_menu(self)
        menu.post(event.x_root, event.y_root)
        menu.focus()

    def __leave_menu(self, menu):
        menu.unpost()
        self.focus()

    @staticmethod
    def __create_context_menu(file):
        menu = Menu(file, tearoff=False)
        menu.add_command(label='Open', command=file.open, underline=0)
        menu.add_separator()
        menu.add_command(label='Rename', command=file.start_renaming, underline=0)
        menu.add_command(label='Delete', command=file.remove, underline=0)
        menu.add_separator()
        menu.add_command(label='Cut', command=file.cut, underline=1)
        menu.add_command(label='Copy', command=file.copy, underline=0)
        menu.add_command(label='Make link', command=file.make_link, underline=0)
        menu.add_separator()
        menu.add_command(label='Properties', command=file.property, underline=0)
        menu.bind('<FocusOut>', lambda e: file.__leave_menu(menu))
        return menu

    def __resend_event_backspace(self):
        self._work_space.focus()
        self.event_generate('<BackSpace>')

    def __resend_event_home(self):
        self._work_space.focus()
        self.event_generate('<Home>')

    def __resend_event_end(self):
        self._work_space.focus()
        self.event_generate('<End>')

    def __bind_file(self):
        self.__canvas.bind('<Double-1>', lambda e: self.open())
        self.__canvas.bind('<Button-1>', lambda event: self.__canvas.focus_set())
        self.__canvas.bind('<FocusIn>', lambda event: self._file_focus_in())
        self.__canvas.bind('<FocusOut>', lambda event: self._file_focus_out())

        self._name.bind('<Button-1>', lambda event: self.start_renaming())
        self._name.bind('<FocusIn>', lambda event: self._file_focus_in())
        self._name.bind('<FocusOut>', lambda event: self._file_focus_out())

        self._name.bind('<Up>', lambda e: self._change_file_focus(-1))
        self._name.bind('<Down>', lambda e: self._change_file_focus(1))
        self.__canvas.bind('<Up>', lambda e: self._change_file_focus(-1))
        self.__canvas.bind('<Down>', lambda e: self._change_file_focus(1))
        # self.bind_all('<Up>', lambda e: self._change_file_focus(-1))
        # self.bind_all('<Down>', lambda e: self._change_file_focus(1))

        self._name.bind('<BackSpace>', lambda e: self.__resend_event_backspace())
        self.__canvas.bind('<BackSpace>', lambda e: self.__resend_event_backspace())
        self._name.bind('<Home>', lambda e: self.__resend_event_home())
        self.__canvas.bind('<Home>', lambda e: self.__resend_event_home())
        self._name.bind('<End>', lambda e: self.__resend_event_end())
        self.__canvas.bind('<End>', lambda e: self.__resend_event_end())

        self._name.bind('<Return>', lambda e: self.open())
        self.__canvas.bind('<Return>', lambda e: self.open())

        self._name.bind('<Delete>', lambda e: self.remove())
        self.__canvas.bind('<Delete>', lambda e: self.remove())

        self._name.bind('<Button-3>', self._context_menu)
        self.__canvas.bind('<Button-3>', self._context_menu)

        self._name.bind('<Control-c>', lambda e: self.copy())
        self.__canvas.bind('<Control-c>', lambda e: self.copy())

        self._name.bind('<Control-x>', lambda e: self.cut())
        self.__canvas.bind('<Control-x>', lambda e: self.cut())

        self._name.bind('<F2>', lambda event: self.start_renaming())
        self.__canvas.bind('<F2>', lambda event: self.start_renaming())
        self.__name_entry.bind('<FocusOut>', lambda event: self.rename())
        self.__name_entry.bind('<Return>', lambda event: self.rename())
        self.__name_entry.bind('<Escape>', lambda event: self.cancel_rename())

    def __configure_canvas(self):
        self.__canvas.pack(fill=BOTH, side=LEFT)
        self._resize_canvas()
        self.__canvas.create_image(0, 0, image=self._icon, anchor=NW)

    def __set_name(self, name=''):
        if name:
            self._name.config(text=name)
        self.__name_entry.pack_forget()
        self._name.pack(fill=BOTH, side=RIGHT)
