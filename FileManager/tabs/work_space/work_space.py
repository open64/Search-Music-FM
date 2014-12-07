__author__ = 'open64'
from tkinter import *
import ttk
from enum import Enum
import os
import shutil
import itertools
from FileManager.tabs.work_space.files.directory import Directory
from FileManager.tabs.work_space.files.simple_file import SimpleFile
import time
if os.name == 'nt':
    import win32api
    import win32con


class DirectoryView(Enum):
    NAME = None
    SIZE = None
    TYPE = None


class WorkSpace(ttk.Frame):
    def __init__(self, window, tabs, path=None):
        ttk.Frame.__init__(self, window)
        self.__tabs = tabs
        self.__bg_color = 'white'
        ttk.Style().configure("TFrame", background=self.__bg_color)

        self.__path = os.getcwd()
        self.__show_hidden_files = False
        self.__buffer = ''
        self.__buffer_operation = ''
        self.__dir_view = DirectoryView.NAME
        self.__curr_focus = 0
        self.__curr_select = None

        self.__file_list = list()
        self.__dir_count = 0
        self.__file_count = 0

        self.x_scrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.y_scrollbar = Scrollbar(self)
        self._canvas = Canvas(
            self, xscrollcommand=self.x_scrollbar.set,
            yscrollcommand=self.y_scrollbar.set,
            bg=self.__bg_color,
            highlightcolor=self.__bg_color,
            highlightbackground=self.__bg_color
        )
        self.max_item_width = 0
        self.max_item_height = 0

        self.x_scrollbar.config(command=self._canvas.xview)
        self.y_scrollbar.config(command=self._canvas.yview)
        self._canvas.pack(side=TOP, anchor=W)
        self.open_directory(path, rename_tab=False)
        self.__create_context_menu()
        self.__bind_word_space()

    def set_buffer(self, new_buffer, operation):
        self.__buffer = new_buffer
        self.__buffer_operation = operation

    def select_focus_file(self, move=0):
        if move:
            new_id = self.__curr_focus + move
            if 0 <= new_id < len(self.__file_list):
                self.__curr_focus = new_id
        self.__file_list[self.__curr_focus].focus()
        self.set_select_file(self.__curr_focus)

    def set_focus_file(self, file_id=0):
        if 0 <= file_id < len(self.__file_list):
            self.__curr_focus = file_id

    def get_focus_file(self):
        return self.__curr_focus

    def set_select_file(self, select=None):
        if select is None or 0 <= select < len(self.__file_list):
            self.__curr_select = select

    def get_select_file(self):
        return self.__curr_select

    def get_file(self, file_id):
        return self.__file_list[file_id]

    def get_canvas(self):
        return self._canvas

    def open_directory(self, path, **kw):
        self.__path = path
        os.chdir(self.__path + os.path.sep)
        self.__show_dir_list()
        if kw.get('rename_tab', True):
            self.__tabs.rename_tab(self.__path, False, True)
        self.focus()
        self.set_focus_file()

    def __get_new_name(self, name, begin, end):
        new_name = name
        count = 2
        while self.__file_list[self.__binary_search(new_name, begin, end)].get_name() == new_name:
            new_name = name + ' %d' % count
            count += 1
        return new_name

    def new_dir(self):
        folder = self.__get_new_name('New folder', 1, self.__dir_count)
        os.mkdir(folder)
        self.__set_new_name(folder, True)

    def new_simple_file(self):
        file = self.__get_new_name('New file', self.__dir_count + 1, self.__dir_count + self.__file_count)
        open(file, 'w').close()
        self.__set_new_name(file, False)

    def __set_new_name(self, name, folder):
        self.open_directory(self.__path)
        if folder:
            file_id = self.__binary_search(name, 1, self.__dir_count)
        else:
            file_id = self.__binary_search(name, self.__dir_count + 1, self.__dir_count + self.__file_count)
        self.set_focus_file(file_id)
        self.select_focus_file()
        self.__file_list[file_id].start_renaming()

    def paste(self):
        path_basename = os.path.basename(self.__buffer)
        paste_name = os.path.join(self.__path, path_basename)
        if self.__buffer_operation == 'cut':
            shutil.move(self.__buffer, paste_name)
        elif self.__buffer_operation == 'copy':
            if self.__buffer == paste_name:
                paste_name += ' (copy)'
            if os.path.isdir(self.__buffer):
                os.mkdir(paste_name)
                self.__copy_dir(self.__buffer, paste_name)
            else:
                shutil.copyfile(self.__buffer, paste_name)
        self.open_directory(self.__path)
        self.set_focus_file()

    @staticmethod
    def __copy_dir(dir_from, dir_to):
        for file in os.listdir(dir_from):
            path_from = os.path.join(dir_from, file)
            path_to = os.path.join(dir_to, file)
            if os.path.isdir(path_from):
                os.mkdir(path_to)
                WorkSpace.__copy_dir(path_from, path_to)
            else:
                shutil.copyfile(path_from, path_to)

    def __binary_search(self, find_element, begin, end):
        while begin < end:
            mid = (begin + end) // 2
            mid_name = self.__file_list[mid-1].get_name()
            if find_element <= mid_name:
                end = mid
            else:
                begin = mid + 1
        return end - 1

    def property(self):
        pass

    def get_path(self):
        return self.__path

    def get_curr_dir(self):
        return os.path.basename(self.__path)

    def _context_menu(self, event):
        self._menu.post(event.x_root, event.y_root)
        self._menu.focus()

    def focus_on_work_space(self):
        self.set_focus_file()
        self.set_select_file()
        self.focus_set()

    def draw_scrollbars(self):
        bbox = self._canvas.bbox(ALL)
        if bbox is not None:
            bb_x0, bb_y0, bb_x1, bb_y1 = bbox
            w = self.winfo_width()
            h = self.winfo_height()
            if h > bb_y1 - bb_y0:
                # no y scrollbar needed
                self.y_scrollbar.place_forget()
                if w < bb_x1 - bb_x0:
                    # x scrollbar needed
                    delta_y = self.x_scrollbar.winfo_reqheight()
                    self.x_scrollbar.place(anchor=SW, rely=1.0, relwidth=1)
                    h -= delta_y
                    if h > bb_y1 - bb_y0:
                        # y scrollbar need finally
                        self.y_scrollbar.place(anchor=NE, relx=1.0, relheight=1, height=-delta_y)
                else:
                    self.x_scrollbar.place_forget()
            else:
                # y scrollbar needed
                delta_x = self.y_scrollbar.winfo_reqwidth()
                w -= delta_x
                if w < bb_x1 - bb_x0:
                    # x scrollbar needed
                    delta_y = self.x_scrollbar.winfo_reqheight()
                    self.x_scrollbar.place(anchor=SW, rely=1.0, relwidth=1, width=-delta_x)
                else:
                    delta_y = 0
                    self.x_scrollbar.place_forget()
                self.y_scrollbar.place(anchor=NE, relx=1.0, relheight=1, height=-delta_y)
        else:
            # no scrollbar needed
            self.y_scrollbar.place_forget()
            self.x_scrollbar.place_forget()

    def __bind_word_space(self):
        self.bind('<Button-3>', self._context_menu)
        self.bind('<Button-1>', lambda event: self.focus_on_work_space())
        self.bind('<Control-v>', lambda event: self.paste())
        self.bind('<Up>', lambda event: self.select_focus_file())
        self.bind('<Down>', lambda event: self.select_focus_file())
        self.bind('<Home>', lambda event: self.__file_list[0].focus())
        self.bind('<End>', lambda event: self.__file_list[-1].focus())
        self._canvas.bind('<FocusIn>', lambda event: self.focus_on_work_space())
        self.bind('<Configure>', lambda event: self.__resize())
        self._menu.bind('<FocusOut>', lambda e: self._menu.unpost())

    def __show_dir_list(self):
        start = time.clock()
        for file in self.__file_list:
            file.destroy()
        if self.__show_hidden_files:
            list_dir = os.listdir(self.__path)
        else:
            list_dir = []
            if os.name[:3] == 'nt':
                for file in os.listdir(self.__path):
                    attr = win32api.GetFileAttributes(file)
                    if attr & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM):
                        continue
                    list_dir.append(file)
            else:
                for file in os.listdir(self.__path):
                    if file.startswith('.'):
                        continue
                    list_dir.append(file)

        size = len(list_dir)
        self.__dir_count = 0
        dir_arr = list(itertools.repeat(0, size))
        self.__file_count = 0
        file_arr = list(itertools.repeat(0, size))
        for file_name in sorted(list_dir, key=self.__dir_view.value):
            if os.path.isdir(file_name):
                dir_arr[self.__dir_count] = Directory(file_name, self.__path, self, bg=self.__bg_color)
                self.__dir_count += 1
            else:
                file_arr[self.__file_count] = SimpleFile(file_name, self.__path, self, bg=self.__bg_color)
                self.__file_count += 1
        self.__file_list = dir_arr[:self.__dir_count] + file_arr[:self.__file_count]
        count = 0
        y = 0
        self._canvas.delete("all")
        for file in self.__file_list:
            file.set_id(count)
            self._canvas.create_window(0, y, window=file, anchor=NW, tags=("all",))
            self._canvas.config(scrollregion=self._canvas.bbox(ALL))
            self.max_item_width = max(self.max_item_width, file.winfo_reqwidth())
            self.max_item_height = max(self.max_item_height, file.winfo_reqheight())
            y += self.max_item_height
            count += 1
        self.draw_scrollbars()
        print(time.clock() - start)

    def __resize(self):
        self._canvas.config(
            width=self.winfo_width() - self.y_scrollbar.winfo_reqwidth(),
            height=self.winfo_height() - self.x_scrollbar.winfo_reqheight()
        )
        self.draw_scrollbars()

    def __create_context_menu(self):
        self._menu = Menu(self, tearoff=False)
        self._menu.add_command(label='New directory', command=self.new_dir, underline=4)
        self._menu.add_separator()
        self._menu.add_command(label='New file', command=self.new_simple_file, underline=4)
        self._menu.add_command(label='Paste', command=self.paste, underline=1)
        self._menu.add_separator()
        self._menu.add_command(label='Properties', command=self.property, underline=0)
