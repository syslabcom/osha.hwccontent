# _+- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from collections import OrderedDict
from osha.hwccontent import vocabularies
from plone import api


class FrontPageView(BrowserView):

    def _get_feed_contents(self, feed_path_from_nav_root=""):
        catalog = api.portal.get_tool(name='portal_catalog')
        nav_root = api.portal.get_navigation_root(self.context)
        feed_folder_path = nav_root.absolute_url_path()\
                           + feed_path_from_nav_root
        num_results = 2
        return catalog.searchResults(
            path=feed_folder_path,
            portal_type="FeedFeederItem",
            sort_limit=num_results,
            sort_on="effective",
            sort_order="descending",
        )[:num_results]

    @property
    def news(self):
        return self._get_feed_contents("/news/combined-feed-folder/")

    @property
    def events(self):
        return self._get_feed_contents("/events/combined-feed-folder/")

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
