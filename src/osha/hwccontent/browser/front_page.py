# _+- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from osha.hwccontent import vocabularies
from plone import api
from plone.app.event.dx.behaviors import IEventLocation

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
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.organisation",
            review_state='published')
        partners = OrderedDict()
        for term in vocabularies.organisation_types:
            partners[term.token] = [[]]

        for result in results:
            try:
                partner = result.getObject()
            except:
                continue
            ot = partner.organisation_type
            if ot not in partners:
                # XXX we should probably log this...
                continue
            # get the last row
            row = partners[ot][-1]
            if len(row) and len(row) % 6 == 0:
                # if the row is "full", create a new one
                partners[ot].append([])
                row = partners[ot][-1]
            row.append(partner)
        return partners

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        try:
            dim = partner.logo.getImageSize()
        except:
            return 'span2'
        if dim and dim[0] < dim[1]:
            return "span2 logovertical"

        return 'span2'
