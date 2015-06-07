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
    dt = datetime.strptime(spec, '%d/%m/%Y')
    return tz.localize(dt)


class JSONEventAccessor(object):
    """Event type generic accessor adapter."""

    implements(IEventAccessor)

    recurrence = ''  # No recurrence support

    def __init__(self, kw, context):
        self.context = ImplicitAcquisitionWrapper(self, context)
        self.url = kw['path']
        self.title = kw['title']
        self.description = u''

        tzname = "Europe/Brussels"
        zone = timezone(tzname)
        self.start = isotime2dt(kw['start_date'], zone)
        self.end = isotime2dt(kw['end_date'], zone)
        self.timezone = tzname

        self.location = kw['City']
        self.attendees = kw['number_of_attendees']  # not used anyway
        self.contact_name = kw['agency_initial_contact']
        self.contact_email = kw['agency_contact_reply']
        self.contact_phone = ""
        self.event_url = kw['website_of_event']
        self.subjects = kw['category'].split(",")
        self.text = kw['body']
        self.organiser = kw['comments_summary_after_eve']
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
        return True

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
        params = {
            'base_url': self.osha_json_url,
            'lang': api.portal.get_tool("portal_languages").getPreferredLanguage(),
            'query_tags': self.remote_event_query_tags,
        }

        date_range = ""
        start, end = self._start_end
        if start:
            date_range = "&start_date[value][date]=" + start.strftime('%d/%m/%Y')
        if end:
            date_range += "&end_date[value][date]=" + end.strftime('%d/%m/%Y')
        params["date_range"] = date_range

        qurl = '{base_url}/{lang}/services/hw/events/{query_tags}?{date_range}'.format(**params)
        items = []
        result = urlopen(qurl)
        if result.code == 200:
            json = load(result)
            for node in json.get("nodes"):
                item = node.get("node")
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
