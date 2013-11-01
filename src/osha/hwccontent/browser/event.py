from DateTime import DateTime
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCatalog.interfaces import ICatalogBrain
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.app.contenttypes.interfaces import ICollection
from plone.app.event.base import date_speller
from plone.app.querystring.querybuilder import QueryBuilder
from plone.memoize import ram
from urllib import urlopen
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements


class EventListing(ListingView):
    implements(IFullWidth)


    def __init__(self, context, request):
        super(EventListing, self).__init__(context, request)
        properties = api.portal.get_tool('portal_properties')
        self.osha_json_url = getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/'
        )
        self.remote_event_query_tags = getattr(
            properties.site_properties,
            'remote_event_query_tags',
            'stress'
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
    
    @ram.cache(ListingView.cache_for_minutes(10))
    def get_remote_events(self):
        """ Queries the OSHA corporate site for events.
            Items returned in JSON format.
        """
        items = []
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()
        qurl = '%s/%s/jsonfeed?portal_type=Event&Subject=%s&path=/osha/portal/%s&Language=%s' \
            % (self.osha_json_url, lang, self.remote_event_query_tags, lang, lang)

        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):
                item['start'] = DateTime(item['startDate'])
                item['end'] = DateTime(item['endDate'])
                
                items.append(item)
        return items

    @ram.cache(ListingView.cache_for_minutes(1))
    def get_local_events(self):
        """ Looks in the current folder for Collection objects and then queries
            them for items.
        """
        items = []
        for child in self.context.values():
            if ICollection.providedBy(child):
                items = self.results(
                    child,
                    batch=False,
                    sort_on='start',
                    brains=True)
        return items

    def get_all_events(self):
        items = self.get_remote_events() + \
            list(self.get_local_events())
        return sorted(
            items,
            key=lambda item: item.__getitem__('start'),
            reverse=True
        )

    def get_batched_events(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        items = self.get_all_events()
        for i in range(b_start, b_size):
            if i >= len(items):
                break
            if ICatalogBrain.providedBy(items[i]):
                item = items[i]
                obj = item.getObject()
                items[i] = {
                    'title': item.Title,
                    'start': item.start,
                    'end': item.end,
                    '_url': item.getURL(),
                    'description': item.Description,
                    'obj': obj
                }
        return Batch(items, b_size, b_start, orphan=1)

    def date_speller(self, date):
        return date_speller(self.context, date)

    def formatted_date(self, occ):
        provider = getMultiAdapter((self.context, self.request, self),
                IContentProvider, name='formatted_date')
        return provider(occ.context)
