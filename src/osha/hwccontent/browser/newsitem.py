from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCatalog.interfaces import ICatalogBrain
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.memoize import ram
from urllib import urlopen
from zope.interface import implements
import base64


class NewsItemListing(ListingView):
    implements(IFullWidth)

    def __init__(self, context, request):
        super(NewsItemListing, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.osha_json_url = getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/'
        )
        self.remote_news_query_tags = getattr(
            properties.site_properties,
            'remote_news_query_tags',
            'stress,hw2014'
        )

    def get_remote_news_items(self):
        """ Queries the OSHA corporate site for news items.
            Items returned in JSON format.
        """
        items = []
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()
        qurl = '%s/%s/jsonfeed?portal_type=News%%20Item&Subject=%s&path=/%s&Language=%s' \
            % (self.osha_json_url, lang, self.remote_news_query_tags, lang, lang)

        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': item['effectiveDate'],
                    'getURL': item['_url'],
                    'Description': item.get('description', ''),
                    'text': item.get('text', ''),
                    'image_base64': item.get('image'),
                    'image_content_type': item.get('image_type')
                })
        return items

    def get_local_news_items(self):
        """ Search for all local news in the default language
        """
        catalog = api.portal.get_tool(name='portal_catalog')
        default_lang = api.portal.get_tool(
            "portal_languages").getDefaultLanguage()
        results = catalog.searchResults(
            portal_type="News Item",
            sort_on="effective",
            sort_order="descending",
            Language=[default_lang, ''],
        )
        return results

    @ram.cache(ListingView.cache_for_minutes(10))
    def get_all_news_items(self):
        items = sorted(
            self.get_remote_news_items() + list(self.get_local_news_items()),
            key=lambda item: item.__getitem__('Date'),
            reverse=True
        )
        for i in range(0, len(items)):
            if ICatalogBrain.providedBy(items[i]):
                item = items[i]
                obj = item.getObject()
                blob = getattr(obj.image, '_blob', None)
                items[i] = {
                    'Title': item.Title,
                    'Date': DateTime(item.Date).utcdatetime(),
                    'getURL': item.getPath(),
                    'Description': item.Description,
                    'text': obj.text and obj.text.output or "",
                    'image': blob and base64.encodestring(blob.open().read()) or None,
                    'obj': obj
                }
            else:
                items[i]['Date'] = DateTime(items[i]['Date']).utcdatetime()
        return items

    def get_batched_news_items(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self.get_all_news_items(), b_size, b_start, orphan=1)
