__author__ = 'open64'


from FileManager.tabs.work_space.files.file import *


class SimpleFile(File):
    IMAGE_PATH = File.IMAGE_PATH + 'file.png'

    def __init__(self, file_name, dir_name, parent, **kw):
        File.__init__(self, file_name, dir_name, parent, **kw)

    def remove(self):
        os.remove(self._name.cget('text'))
        File.remove(self)

    def set_default_icon(self):
        self._icon.config(file=SimpleFile.IMAGE_PATH)
        self._resize_canvas()

    def _get_default_image(self):
        return SimpleFile.IMAGE_PATH
