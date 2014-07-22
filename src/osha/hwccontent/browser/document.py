# _+- coding: utf-8 -*-

from plone import api
from zope.component import getMultiAdapter
from zope.interface import implements

from Acquisition import aq_parent
from Products.Five.browser import BrowserView

from osha.hwccontent.browser.utils import get_partners, css_by_orientation
from osha.hwccontent.interfaces import IFullWidth

import random

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

    def get_partner_start(self):
        return random.randint(1, 6)

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)


class OrganisationsAtozView(BrowserView):
    implements(IFullWidth)

    def partners(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.organisation",
            Language='all',
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
            scaling = getMultiAdapter((fop, self.request), name='images')
            if scaling.getImageSize('logo') == (-1, -1):
                scaling = None
            letters[letter][title] = dict(
                url=fop.absolute_url(), scaling=scaling)

        for letter in letters:
            letters[letter] = OrderedDict(sorted(
                letters[letter].items(), key=lambda t: t[0].lower()))

        return letters

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
            Language='all',
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

        for letter in letters:
            letters[letter] = OrderedDict(sorted(
                letters[letter].items(), key=lambda t: t[0].lower()))

        return letters


class MediaPartnersView(BrowserView):
    implements(IFullWidth)

    def partners(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.mediapartner",
            Language='all',
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
            scaling = getMultiAdapter((fop, self.request), name='images')
            if scaling.getImageSize('logo') == (-1, -1):
                scaling = None
            letters[letter][title] = dict(
                url=fop.absolute_url(), scaling=scaling)

        for letter in letters:
            letters[letter] = OrderedDict(sorted(
                letters[letter].items(), key=lambda t: t[0].lower()))

        return letters

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)
