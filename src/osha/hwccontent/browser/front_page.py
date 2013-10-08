# _+- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from osha.hwccontent import vocabularies
from plone import api

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class FrontPageView(BrowserView):

    def news(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        num_results = 2
        return catalog.searchResults(
            portal_type="News Item",
            sort_limit=num_results,
            sort_on="effective",
            sort_order="descending",
        )[:num_results]

    def events(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        num_results = 2
        return catalog.searchResults(
            portal_type="Event",
            sort_limit=num_results,
            sort_on="start",
            sort_order="descending",
        )[:num_results]

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
