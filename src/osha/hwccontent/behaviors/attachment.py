# -*- coding: utf-8 -*-
from osha.hwccontent import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.multilingualbehavior import directives
from plone.namedfile.field import NamedBlobFile
from plone.supermodel import model
from zope import interface
from zope.component import adapts


@interface.provider(IFormFieldProvider)
class IAttachmentField(model.Schema):
    """Marker / Form interface for attachment field"""

    attachment = NamedBlobFile(
        title=_(u"Attachment"),
        description=u"Select an attachment to be uploaded (e.g. a PDF file).",
        required=False,
    )

    directives.languageindependent('attachment')


@interface.implementer(IAttachmentField)
class AttachmentField(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
