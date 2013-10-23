# _+- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from osha.hwccontent import vocabularies
from plone import api
from plone.app.event.dx.behaviors import IEventLocation
from osha.hwccontent.browser.utils import get_partners, css_by_orientation

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class FrontPageView(BrowserView):

    def news(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        num_results = 2
        results = catalog.searchResults(
            portal_type="News Item",
            sort_limit=num_results,
            sort_on="effective",
            sort_order="descending",
        )[:num_results]
        return [x.getObject() for x in results]

    def events(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        num_results = 2
        results = catalog.searchResults(
            portal_type="plone.app.event.dx.event",
            sort_limit=num_results,
            sort_on="start",
            sort_order="descending",
        )[:num_results]
        return [x.getObject() for x in results]

    def get_event_location(self, event):
        """For some reason, this behavior-induced field is not accessible
            directly on the event.
        """
        try:
            event = IEventLocation(event)
            return event.location
        except TypeError:
            return None

    def partners(self):
        return get_partners()


    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)
    