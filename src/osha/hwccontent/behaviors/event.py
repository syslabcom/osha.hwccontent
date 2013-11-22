# -*- coding: utf-8 -*-

from plone.supermodel import model
from plone.autoform.interfaces import IFormFieldProvider
from zope import schema
from zope.interface import alsoProvides
from osha.hwccontent import _


class IEventOrganiser(model.Schema):
    """Event summary (body text) schema."""

    organiser = schema.TextLine(
        title=_('Organiser'),
        description=_(
            u'help_event_organiser',
            default=u'The organiser of this meeting'
        ),
        required=True,
    )

alsoProvides(IEventOrganiser, IFormFieldProvider)
