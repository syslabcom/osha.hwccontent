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
            'stress+hw2014'
        )

    @ram.cache(ListingView.cache_for_minutes(10, 'publication'))
    def get_remote_publications(self):
        """ Queries the OSHA corporate site for news items.
            Items returned in JSON format.
        """
        items = []
        params = {
            "base_url": self.osha_json_url,
            "lang": self.lang,
            "query_tags": self.remote_publication_query_tags,
        }
        qurl = "{base_url}/{lang}/services/hw/publications/{query_tags}".format(**params)
        result = urlopen(qurl)
        if result.code == 200:
            json = load(result)
            for node in json.get("nodes"):
                item = node.get("node")
                file_path = item.get("file", "")
                if file_path:
                    filename = file_path.split("/")[-1]
                else:
                    filename = ""
                pd = item.get('publication_date', '')
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': (
                        pd and DateTime(pd, datefmt="international").strftime(
                            "%Y/%m/%d %H:%M") or ""),
                    'getURL': item.get('path'),
                    'path': item.get('path'),
                    'Description': item.get('body', ''),
                    'remote_image': item.get('cover_image_thumbnail', ''),
                    'node_id': item.get('nid'),
                    'filename': filename,
                    'file_size': item.get('file_size', ""),
                    'file_content_type': item.get('file_content_type', "application/pdf"),
                })
        return items

    def get_batched_publications(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self.get_remote_publications(), b_size, b_start, orphan=1)
