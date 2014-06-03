from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from json import load
from osha.hwccontent.interfaces import IMaterialsView
from osha.hwccontent.browser.mixin import ListingView
from plone.memoize import ram
from urllib import urlopen
from zope.interface import implements
from plone import api


class PublicationListing(ListingView):
    implements(IMaterialsView)

    def __init__(self, context, request):
        super(PublicationListing, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.remote_publication_query_tags = getattr(
            properties.site_properties,
            'remote_publication_query_tags',
            'stress,hw2014'
        )

    @ram.cache(ListingView.cache_for_minutes(10, 'publication'))
    def get_remote_publications(self):
        """ Queries the OSHA corporate site for news items.
            Items returned in JSON format.
        """
        items = []
        qurl = '%s/%s/jsonfeed?portal_type=File&Subject=%s&path=/%s' \
                '&Language=%s&object_provides=slc.publications.interfaces' \
                '.IPublicationEnhanced' % (
                    self.osha_json_url,
                    self.lang,
                    self.remote_publication_query_tags,
                    self.lang,
                    self.lang,
                )
        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': DateTime(item['effectiveDate']).utcdatetime(),
                    'getURL': item['_url'],
                    'Description': item.get('description', ''),
                    'image_base64': item.get('cover_image'),
                    'image_content_type': item.get(
                        '_cover_image_content_type'),
                    'filename': item.get('_file_filename'),
                    'file_size': item.get('_file_file_size'),
                    'file_content_type': item.get('_file_content_type'),
                })
        return items

    def get_batched_publications(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self.get_remote_publications(), b_size, b_start, orphan=1)
