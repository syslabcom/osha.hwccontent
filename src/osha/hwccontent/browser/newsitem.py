from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCatalog.interfaces import ICatalogBrain
from five import grok
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.app.contenttypes.interfaces import INewsItem
from plone.directives import dexterity
from plone.memoize import ram
from time import time
from urllib import urlopen
from zope.interface import Interface
from zope.interface import implements

grok.templatedir("templates")


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
        params = {
            "base_url": self.osha_json_url,
            "lang": api.portal.get_tool("portal_languages").getPreferredLanguage(),
            "query_tags": self.remote_news_query_tags,
        }
        qurl = "{base_url}/{lang}/services/hw/news/{query_tags}".format(**params)
        result = urlopen(qurl)
        if result.code == 200:
            json = load(result)
            for node in json.get("nodes"):
                item = node.get("node")
                pd = item.get('publication_date', '')
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': (
                        pd and DateTime(pd, datefmt="international").strftime(
                            "%Y/%m/%d %H:%M") or ""),
                    'getURL': item.get('path'),
                    'path': item.get('path'),
                    'Description': item.get('summary', '') or item.get('body', ''),
                    'text': item.get('summary', '') and item.get('body', '') or '',
                    'remote_image': item.get('image', ''),
                    'node_id': item.get('nid'),
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
            review_state='published',
            Language=[default_lang, ''],
        )
        return results

    @ram.cache(ListingView.cache_for_minutes(10, 'newsitem'))
    def get_all_news_items(self):
        local_news = list(self.get_local_news_items())
        for news in local_news:
            news['Date'] = (news['Date'] and DateTime(
                news['Date'],
                datefmt="international").strftime("%Y/%m/%d %H:%M") or "")
        allnews = self.get_remote_news_items() + local_news
        items = sorted(
            allnews,
            key=lambda item: item.__getitem__('Date'),
            reverse=True
        )
        for i in range(0, len(items)):
            if ICatalogBrain.providedBy(items[i]):
                item = items[i]
                obj = item.getObject()
                has_image = getattr(obj.image, '_blob', False)
                image_url = ''
                if has_image:
                    image_url = obj.absolute_url() + "/@@images/image/preview"
                items[i] = {
                    'Title': item.Title,
                    'Date': DateTime(item.Date).utcdatetime(),
                    'getURL': item.getURL(),
                    'Description': item.Description,
                    'text': obj.text and obj.text.output or "",
                    'image_url': image_url,
                    'image_caption': obj.image_caption if has_image else '',
                    'obj': obj,
                    'is_local': True,
                }
            else:
                items[i]['Date'] = DateTime(items[i]['Date']).utcdatetime()
        return items

    def get_batched_news_items(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self.get_all_news_items(), b_size, b_start, orphan=1)


class RemoteNewsItem(grok.View):
    implements(IFullWidth)
    grok.name('remote-news-item')
    grok.context(Interface)
    grok.template("remote_news_item")

    def __init__(self, context, request):
        super(RemoteNewsItem, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.osha_json_url = getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/'
        )

    @ram.cache(lambda method, self, node_id: (node_id, time() // (60 * 60 * 24)))
    def get_remote_news_item(self, node_id):
        """ Queries the OSHA corporate site for a particular news item, which is returned in JSON
        format.

        While it would be possible to cache the results of NewsItemListing.get_remote_news_items and
        look up the details for the relevant news item, it's complicated because the results are
        batched. Caching for a day based on the node id, should be sufficient.
        """
        items = []
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()

        params = {
            "base_url": self.osha_json_url,
            "lang": lang,
            "node_id": node_id,
        }
        qurl = "{base_url}/{lang}/services/hw/news1/{node_id}".format(**params)

        result = urlopen(qurl)
        if result.code == 200:
            json = load(result)
            for node in json.get("nodes"):
                item = node.get("node")
                pd = item.get('publication_date', '')
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': (
                        pd and DateTime(pd, datefmt="international").strftime(
                            "%Y/%m/%d %H:%M") or ""),
                    'getURL': item.get('path'),
                    'Description': item.get('summary', ''),
                    'text': item.get('body', ''),
                    'remote_image': item.get('image', ''),
                })
        if len(items) > 0:
            return items.pop()


class AddForm(dexterity.AddForm):
    grok.name('News Item')
    grok.require('plone.app.contenttypes.addNewsItem')

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        fname = 'IDublinCore.description'
        self.widgets[fname].field.description = u"Write a short summary. "\
            u"This will appear on the homepage of the campaign site."


class EditForm(dexterity.EditForm):
    grok.context(INewsItem)
    grok.require("cmf.ModifyPortalContent")

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        fname = 'IDublinCore.description'
        self.widgets[fname].field.description = u"Write a short summary. "\
            u"This will appear on the homepage of the campaign site."
