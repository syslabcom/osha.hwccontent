# -*- coding: utf-8 -*-

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
