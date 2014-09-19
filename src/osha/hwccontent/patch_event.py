# -*- coding: utf-8 -*-

from plone.app.event.browser import event_view
from plone.app.contenttypes.interfaces import IEvent
from osha.hwccontent.behaviors.event import IEventLocation
from osha.hwccontent.interfaces import IEventAccessor


def get_location(context):
    """Return the location, using our own field"""
    location = u""
    if IEvent.providedBy(context):
        data = IEventLocation(context)
        location = data.location
    elif IEventAccessor.providedBy(context):
        location = context.location
    return location


event_view.get_location = get_location
