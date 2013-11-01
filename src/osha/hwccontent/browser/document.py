# _+- coding: utf-8 -*-

from datetime import datetime
from json import load
from urllib import urlopen
from urlparse import urljoin

from plone import api
from zope.interface import implements
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from plone.app.textfield.interfaces import ITransformer
from plone.app.textfield.value import RichTextValue

from osha.hwccontent.browser.utils import get_partners, css_by_orientation, isotime2dt
from osha.hwccontent.interfaces import IFullWidth

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class FilesView(BrowserView):

    def get_files(self):
        files = [
            x for x in aq_parent(self.context).objectValues()
            if x.portal_type == 'File']
        return files


class OrganisationsView(BrowserView):
    implements(IFullWidth)

    def partners(self):
        return get_partners()

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)


class FocalPointsView(BrowserView):
    implements(IFullWidth)

    def focalpoints(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.focalpoint",
            review_state='published')

        letters = {}

        for result in results:
            try:
                fop = result.getObject()
            except:
                continue
            country = fop.country
            letter = country[0].lower()
            if letter not in letters:
                letters[letter] = {}
            letters[letter][country] = fop.absolute_url()
        return letters
