# _+- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from osha.hwccontent.browser.utils import get_partners, css_by_orientation


class FilesView(BrowserView):

    def get_files(self):
        files = [
            x for x in aq_parent(self.context).objectValues()
            if x.portal_type == 'File']
        return files

    
class OrganisationsView(BrowserView):
    
    def partners(self):
        return get_partners()
    
    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)
        