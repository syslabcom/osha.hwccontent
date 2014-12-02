from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCatalog.interfaces import ICatalogBrain
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.app.contenttypes.interfaces import ICollection
from plone.app.querystring.querybuilder import QueryBuilder
from plone.app.textfield.interfaces import ITransformer
from plone.app.textfield.value import RichTextValue
from plone.memoize import ram
from urllib import urlopen
from zope.interface import implements

import base64


class PressReleaseListing(ListingView):
    implements(IFullWidth)

    def __init__(self, context, request):
        super(PressReleaseListing, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.osha_json_url = getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/'
        )
        self.remote_press_release_query_tags = getattr(
            properties.site_properties,
            'remote_press_release_query_tags',
            'Campaign%202012-13'
        )

    def results(self, collection, batch=True, b_start=0, b_size=None,
                sort_on=None, limit=None, brains=False):
        # XXX This code is from plone.app.contenttypes.content.py, we need this
        # here until my pull request is merged.
        # https://github.com/plone/plone.app.contenttypes/pull/87
        querybuilder = QueryBuilder(collection, self.request)
        sort_order = 'reverse' if collection.sort_reversed else 'ascending'
        if not b_size:
            b_size = collection.item_count
        if not sort_on:
            sort_on = collection.sort_on
        if not limit:
            limit = collection.limit
        return querybuilder(
            query=collection.query, batch=batch, b_start=b_start, b_size=b_size,
            sort_on=sort_on, sort_order=sort_order,
            limit=limit, brains=brains
        )

    @ram.cache(ListingView.cache_for_minutes(10, 'pressrelease'))
    def get_remote_press_releases(self):
        """ Queries the OSHA corporate site for press releases.
            Items returned in JSON format.
        """
        items = []
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()
        qurl = '%s/%s/jsonfeed?portal_type=PressRelease&Subject=%s&path=/%s&Language=%s' \
            % (self.osha_json_url, lang, self.remote_press_release_query_tags, lang, lang)

        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):
                items.append({
                    'remote_item': True,
                    'Title': item['title'],
                    'Date': item['effectiveDate'],
                    'getURL': item['_url'],
                    'Description': item.get('description', ''),
                    'image_base64': item.get('image'),
                    'image_content_type': item.get('image_type'),
                    'text': self.make_intro(self.make_plain_text(item)),

                })
        return items

    @ram.cache(ListingView.cache_for_minutes(10, 'pressrelease'))
    def get_local_press_releases(self):
        """ Looks in the current folder for Collection objects and then queries
            them for items.
        """
        items = []
        for child in self.context.values():
            if ICollection.providedBy(child):
                items = self.results(
                    child,
                    batch=False,
                    sort_on='Date',
                    brains=True)
        return items

    def get_all_press_releases(self):
        items = self.get_remote_press_releases() + \
            list(self.get_local_press_releases())
        return sorted(
            items,
            key=lambda item: item.__getitem__('Date'),
            reverse=True
        )

    def get_batched_press_releases(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        items = self.get_all_press_releases()
        for i in range(b_start, b_size):
            if i >= len(items):
                break
            if ICatalogBrain.providedBy(items[i]):
                item = items[i]
                obj = item.getObject()
                blob = getattr(obj.image, '_blob', None)
                plain_text = obj.restrictedTraverse('@@text-transform/text/text/plain')
                items[i] = {
                    'Title': item.Title,
                    'Date': DateTime(item.Date).utcdatetime(),
                    'getURL': item.getURL(),
                    'Description': item.Description,
                    'image': blob and base64.encodestring(blob.open().read()) or None,
                    'obj': obj,
                    'text': self.make_intro(plain_text),
                }
            else:
                items[i]['Date'] = DateTime(items[i]['Date']).utcdatetime()
        return Batch(items, b_size, b_start, orphan=1)

    def make_plain_text(self, item):
        text = item.get('text')
        if not text:
            return ''

        transformer = ITransformer(self.context)
        value = RichTextValue(text, mimeType=item.get('_text_mime_type', 'text/html'))
        return transformer(value, 'text/plain')

    def make_intro(self, text):
        if len(text) < 200:
            return text

        text = text[:200].rsplit(None, 1)[0]
        return text + u'...'
