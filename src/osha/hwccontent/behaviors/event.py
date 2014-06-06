# -*- coding: utf-8 -*-

from plone.app.event.dx.behaviors import IEventLocation as IBaseEventLocation
from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import alsoProvides


class IEventOrganiser(model.Schema):
    """Event summary (body text) schema."""

    organiser = schema.TextLine(
        title=u'Organiser',
        description=u'The organiser of this meeting',
        required=True,
    )

alsoProvides(IEventOrganiser, IFormFieldProvider)


class IEventLocation(IBaseEventLocation):
    location = schema.TextLine(
        title=u'Location',
        description=u'OSHA Location of the event.',
        required=True,
    )
alsoProvides(IEventLocation, IFormFieldProvider)
