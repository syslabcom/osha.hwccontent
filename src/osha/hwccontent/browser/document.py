# _+- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five.browser import BrowserView


class FilesView(BrowserView):

    def get_files(self):
        files = [
            x for x in aq_parent(self.context).objectValues()
            if x.portal_type == 'File']
        return files
