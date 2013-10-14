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
        
    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner. 
            Requested by maite through erral, so that we can set a special class
        """
        try:
            dim = partner.logo.getImageSize()
        except:
            return 'span2'
        if dim and dim[0]<dim[1]:
            # portrait, see https://github.com/syslabcom/hw2014theme/commit/1de7b5863c7770964a7f22689b9041fb0726f1d4#diff-50e2b6e3fa87897791e8aad1cbcf9893L282
            return "span2 logovertical"
            
        return 'span2'