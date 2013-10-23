# -*- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IEvent
from plone.indexer.decorator import indexer
from plone.app.event.dx.behaviors import IEventLocation


@indexer(IEvent)
def location(obj):
    try:
        adapted = IEventLocation(obj)
        return adapted.location
    except TypeError:
        return ""
