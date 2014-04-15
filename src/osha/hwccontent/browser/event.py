from Acquisition import ImplicitAcquisitionWrapper
from Products.CMFPlone.PloneBatch import Batch
from Products.CMFCore.utils import getToolByName
from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from datetime import datetime, timedelta
from five import grok
from json import load
from osha.hwccontent.browser.mixin import ListingView
from osha.hwccontent.interfaces import IFullWidth
from osha.hwccontent.behaviors.event import IEventOrganiser
from plone import api
from plone.directives import dexterity
from plone.memoize import ram
from plone.app.contenttypes.interfaces import IEvent
from plone.app.event.browser.event_listing import EventListing
from plone.app.event.base import (
    get_events,
    RET_MODE_ACCESSORS,
)
from plone.app.layout.navigation.root import getNavigationRootObject
from plone.multilingual.interfaces import (
    ITranslationManager,
    ITranslatable,
)
from osha.hwccontent.interfaces import IEventAccessor
from pytz import timezone
from urllib import urlencode
from urllib import urlopen
from zope.interface import implements
from zope.component.hooks import getSite


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

    recurrence = ''  # No recurrence support

    def __init__(self, kw, context):
        self.context = ImplicitAcquisitionWrapper(self, context)
        self.created = kw['creation_date']
        self.last_modified = kw['modification_date']
        self.url = kw['_url']
        self.title = kw['title']
        self.description = u''

        tz = kw['startDate'][-6:]
        minutes = tz[-2:]
        hours = tz[-5:-3]
        seconds = int(minutes) * 60 + int(hours) * 3600
        if tz[0] == '-':
            seconds = -seconds
        offset = timedelta(seconds=seconds)

        # We try CET first, because it's most common, and if none works, we use CET anyway.
        # So Brussels should be both first and last in this list:
        for tzname in ['Europe/Brussels', 'Europe/London', 'Europe/Helsinki', 'Atlantic/Reykjavik']:  # , 'Europe/Brussels']:
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
        self.organiser = kw['description']

        if kw.get('attachment', None):
            self.attachment = True
            self.attachment_content_type = kw.get('_attachment_content_type')
            self.attachment_filename = kw.get('_attachment_filename')
            mtr = getToolByName(context, "mimetypes_registry")
            mime = list(mtr.lookup(self.attachment_content_type))
            mime.append(mtr.lookupExtension(self.attachment_filename))
            mime.append(mtr.lookup("application/octet-stream")[0])

            portal_url = api.portal.get().absolute_url()
            icon_paths = [m.icon_path for m in mime if m.icon_path]
            if icon_paths:
                self.attachment_icon = portal_url + "/" + icon_paths[0]
            else:

                self.attachment_icon = portal_url + "/" + guess_icon_path(mime[0])
        else:
            self.attachment = False

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
        return self.end - self.start


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

    @ram.cache(ListingView.cache_for_minutes(10, 'event'))
    def get_all_events(self, batch=True):
        # Fall back to default language for local events
        kw = {}
        default_lang = api.portal.get_tool(
            "portal_languages").getDefaultLanguage()
        if ITranslatable.providedBy(self.context):
            if default_lang != self.context.Language():
                portal = getSite()
                trans = ITranslationManager(self.context).get_translation(
                    default_lang)
                root = getNavigationRootObject(trans, portal)
                kw['path'] = '/'.join(root.getPhysicalPath())
                kw['Language'] = [default_lang, '']
        start, end = self._start_end
        sort = 'start'
        sort_reverse = False
        if self.mode in ('past', 'all'):
            sort_reverse = True
        expand = True
        local_events = get_events(
            self.context, start=start, end=end, sort=sort, review_state='published',
            sort_reverse=sort_reverse, ret_mode=RET_MODE_ACCESSORS,
            expand=expand, **kw)

        remote_events = self._remote_events()
        reverse = self.mode == 'past'
        all_events = sorted(local_events + remote_events, key=lambda x: x.start, reverse=reverse)
        if batch:
            b_start = self.b_start
            b_size = self.b_size
            res = Batch(all_events, size=b_size, start=b_start, orphan=self.orphan)
        else:
            res = all_events
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
        result = urlopen(qurl)
        if result.code == 200:
            for item in load(result):
                items.append(JSONEventAccessor(item, self))
        return items

    def get_organiser(self, event):
        if isinstance(event, JSONEventAccessor):
            return event.organiser
        data = IEventOrganiser(event.context)
        return data.organiser


class AddForm(dexterity.AddForm):
    grok.name('Event')
    grok.require('plone.app.contenttypes.addEvent')

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        fname = 'IDublinCore.description'
        self.widgets[fname].field.description = u"Write a short summary. "\
            u"This will appear on the homepage of the campaign site."


class EditForm(dexterity.EditForm):
    grok.context(IEvent)
    grok.require("cmf.ModifyPortalContent")

    def updateWidgets(self):
        super(EditForm, self).updateWidgets()
        fname = 'IDublinCore.description'
        self.widgets[fname].field.description = u"Write a short summary. "\
            u"This will appear on the homepage of the campaign site."
