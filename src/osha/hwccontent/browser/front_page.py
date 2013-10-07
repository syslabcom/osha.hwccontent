# _+- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
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
        partners = list()
        row = list()
        i = 0
        for result in results:
            if i > 0 and i % 6 == 0:
                partners.append(row)
                row = list()
            try:
                partner = result.getObject()
            except:
                continue
            row.append(partner)
            i += 1
        partners.append(row)
        return partners
