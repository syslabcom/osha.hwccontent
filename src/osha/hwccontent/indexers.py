# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from plone.app.event.dx.behaviors import IEventLocation

from osha.hwccontent.organisation import IOrganisation


@indexer(IEvent)
def location(obj):
    try:
        adapted = IEventLocation(obj)
        return adapted.location
    except TypeError:
        return ""


@indexer(IOrganisation)
def key_email(obj):
    return getattr(obj, 'key_email')
