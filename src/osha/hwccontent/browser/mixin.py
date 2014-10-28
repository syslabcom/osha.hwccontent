from plone import api
from Products.Five.browser import BrowserView
from plone.dexterity.interfaces import IDexterityContent
from osha.hwccontent.utils import get_storage_cachekey
from osha.hwccontent.browser.helper import get_path_to_icon
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
        self.lang = api.portal.get_tool(
            "portal_languages").getPreferredLanguage()
        self.user = api.user.get_current()

    def can_edit(self, obj):
        """ helper view to determine if the user can edit the current object"""
        return not api.user.is_anonymous() and \
            IDexterityContent.providedBy(obj) and self.user.checkPermission(
                'Modify portal content', obj)

    def show_remote_url(self, obj):
        """ helper view to determine if the the object was syndicated
        and the current user should see the remote url"""
        return not api.user.is_anonymous() and \
            not IDexterityContent.providedBy(obj) and \
            'Manager' in api.user.get_roles()

    def get_icon_path(self, obj=None, content_type=None):
        return get_path_to_icon(obj, content_type)

    @staticmethod
    def cache_for_minutes(minutes, for_type):
        """ Generates a cachekey which won't change for $minutes amount of time
            as well as the preferred language.
        """

        def _cachekey(method, self, batch=True):
            mode = self.request.get('mode', '')
            b_start = self.request.get('b_start', '')
            date = self.request.get('date', '')
            key = (
                get_storage_cachekey(for_type),
                time() // (60 * minutes),
                self.lang,
                batch,
                mode,
                b_start,
                date,
                self.request.get('SERVER_URL', ''),
            )
            return key

        return _cachekey
