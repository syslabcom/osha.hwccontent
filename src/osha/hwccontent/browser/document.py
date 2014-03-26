# _+- coding: utf-8 -*-

from plone import api
from zope.interface import implements
from Acquisition import aq_parent
from Products.Five.browser import BrowserView

from osha.hwccontent.browser.utils import get_partners, css_by_orientation
from osha.hwccontent.interfaces import IFullWidth

import random


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

    def get_partner_start(self):
        return random.randint(1, 6)

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


class MediaPartnersView(BrowserView):
    implements(IFullWidth)

    def partners(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.mediapartner",
            review_state='published')

        letters = {}

        for result in results:
            try:
                fop = result.getObject()
            except:
                continue
            title = fop.title
            letter = title[0].lower()
            if letter not in letters:
                letters[letter] = {}
            letters[letter][title] = fop.absolute_url()
        return letters

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)
