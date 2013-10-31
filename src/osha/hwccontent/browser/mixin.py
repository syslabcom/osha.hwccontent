from plone import api
from Products.Five.browser import BrowserView
from time import time


class ListingView(BrowserView):
    """ Reusable methods for listing type views.
    """
    
    def __init__(self, context, request):
        super(ListingView, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.osha_json_url = getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/'
        )
        self.lang = api.portal.get_tool("portal_languages").getPreferredLanguage()


    @staticmethod
    def cache_for_minutes(minutes):
        """ Generates a cachekey which won't change for $minutes amount of time
            as well as the preferred language.
        """

        def _cachekey(method, self):
            return time() // (60*minutes), self.lang

        return _cachekey
