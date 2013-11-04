from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFPlone.PloneBatch import Batch
from Products.ZCatalog.interfaces import ICatalogBrain
from datetime import datetime, timedelta
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from plone import api
from plone.app.contenttypes.interfaces import ICollection
from plone.app.event.base import date_speller
from plone.app.event.browser.event_listing import EventListing
from plone.app.event.dx.behaviors import EventAccessor
from plone.app.querystring.querybuilder import QueryBuilder
from plone.event.interfaces import IEventAccessor
from plone.memoize import ram
from pytz import timezone
from urllib import urlencode
from urllib import urlopen
from zope.component import getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import implements
        
def isotime2dt(isotime, tz):
    separator = isotime[-6]
    if separator in '+-':
        # Take off the timezone
        spec = isotime.rsplit(separator, 1)[0]
    else:
        spec = isotime
    dt = datetime.strptime(spec, '%Y-%m-%dT%H:%M:%S')
    return tz.localize(dt)
    

class JSONEventAccessor(object):
    """Event type generic accessor adapter."""

    implements(IEventAccessor)

    recurrence = '' # No recurrence support

    def __init__(self, kw, context):
        self.context = ImplicitAcquisitionWrapper(self, context)
        self.created = kw['creation_date']
        self.last_modified = kw['modification_date']
        self.url = kw['_url']
        self.title = kw['title']
        self.description = kw['description']

        tz = kw['startDate'][-6:]
        minutes = tz[-2:]
        hours = tz[-5:-3]
        seconds = int(minutes)*60 + int(hours)*3600
        if tz[0] == '-':
            seconds = -seconds
        offset = timedelta(seconds=seconds)

        # We try CET first, because it's most common, and if none works, we use CET anyway.
        # So Brussels should be both first and last in this list:
        for tzname in ['Europe/Brussels', 'Europe/London', 'Europe/Helsinki', 'Atlantic/Reykjavik']:#, 'Europe/Brussels']:
            zone = timezone(tzname)
            if tz[0] not in '-+':
                # Naive date time, just assume CET
                break
            
            # Verify this:
            if isotime2dt(kw['startDate'], zone).utcoffset() == offset:
                break 
        
        self.start = isotime2dt(kw['startDate'], zone)
        self.end = isotime2dt(kw['endDate'], zone)
        self.timezone = tzname
        
        self.location = kw['location']
        self.attendees = kw['attendees']
        self.contact_name = kw['contactName']
        self.contact_email = kw['contactEmail']
        self.contact_phone = kw['contactPhone']
        self.event_url = kw['eventUrl']
        self.subjects = kw['subject']
        self.text = kw['text']

    # Unified create method via Accessor
    @classmethod        
    def create(self, **kw):
        return JSONEventAccessor(kw)

    @property
    def uid(self):
        return None
    
    @property
    def whole_day(self):
        return False

    @property
    def open_end(self):
        return False
                
    @property
    def duration(self):
        return end - start


class EventListing(ListingView, EventListing):
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

    def events(self, ret_mode=3, batch=True):
        local_events = self._get_events(3) # Only accessors works with remote events.
        remote_events = self._remote_events()
        reverse = self.mode == 'past'
        all_events = sorted(local_events + remote_events, key=lambda x: x.start, reverse=reverse)
        if batch:
            b_start = self.b_start
            b_size  = self.b_size
            res = Batch(all_events, size=b_size, start=b_start, orphan=self.orphan)
        return res

    def _remote_events(self):
        """ Queries the OSHA corporate site for events.
            Items returned in JSON format.
        """
        items = []
        lang = api.portal.get_tool("portal_languages").getPreferredLanguage()
        start, end = self._start_end
        q = {'portal_type': 'Event',
             'Subject': self.remote_event_query_tags,
             'path': '/osha/portal/' + lang,
             'Language': lang}
        if start:
            q['start'] = start.strftime('%Y-%m-%dT%H:%M:%S%z')
        if end:
            q['end'] = end.strftime('%Y-%m-%dT%H:%M:%S%z')
        
        qurl = '%s/%s/jsonfeed?' % (self.osha_json_url, lang)
        qurl += urlencode(q)
        print qurl
        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):                
                items.append(JSONEventAccessor(item, self))
        return items
