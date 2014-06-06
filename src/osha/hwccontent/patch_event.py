# -*- coding: utf-8 -*-

from plone.app.event.browser import event_view
from osha.hwccontent.behaviors.event import IEventLocation


def get_location(context):
    """Return the location, using our own field"""
    data = IEventLocation(context)
    return data.location

event_view.get_location = get_location
