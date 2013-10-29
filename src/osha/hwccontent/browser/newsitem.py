from Products.CMFPlone.PloneBatch import Batch
from Products.Five.browser import BrowserView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.app.contenttypes.interfaces import ICollection
from plone.app.querystring.querybuilder import QueryBuilder
from zope.interface import implements


class NewsItemListing(BrowserView):
    implements(IFullWidth)

    def remote_url(self):
        properties = api.portal.get_tool('portal_properties')
        return getattr(
            properties.site_properties,
            'osha_json_url',
            'https://osha.europa.eu/')

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

    def get_all_news_items(self):
        # TODO: this needs to be cached.
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()
        qurl = self.remote_url() + \
            '/jsonfeed?portal_type=NewsItem&path=/%s&Subject=%s&Language=%s' \
            % (lang, ','.join(self.context.Subject()), lang)

        items = []
        for child in self.context.values():
            if ICollection.providedBy(child):
                items = self.results(
                    child,
                    batch=False,
                    sort_on='Date',
                    brains=True)

        # TODO: JSON view needs to be available on OSHA corp.
        # result = urlopen(qurl)
        # if result.code == '200':
        #     for item in load(result):
        #         items.append({
        #             'Title': item['title'],
        #             'Date': datetime.strptime(item['releaseDate'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
        #             'getURL': item['_url'],
        #             'Description': getattr(item, 'text', '')
        #         })
        return sorted(items, key=lambda item: getattr(item, 'Date'))

    def get_batched_news_items(self):
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self.get_all_news_items(), b_size, b_start, orphan=1)

