__author__ = 'open64'
from FileManager.tabs.work_space.files.file import File
import os
import shutil


class Directory(File):
    IMAGE_PATH = File.IMAGE_PATH + 'dir.png'

    def __init__(self, file_name, dir_name, parent, **kw):
        File.__init__(self, file_name, dir_name, parent, **kw)

    def _get_default_image(self):
        return Directory.IMAGE_PATH

    def remove(self):
        shutil.rmtree(self._name.cget('text'))
        File.remove(self)

    def open(self, **kw):
        if self._dir == os.path.sep:
            path = self._dir + self._name.cget('text')
        else:
            path = self._dir + os.path.sep + self._name.cget('text')
        self._work_space.open_directory(path, **kw)
