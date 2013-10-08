# _+- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from osha.hwccontent.interfaces import ISectionIntro
from plone.app.contenttypes.interfaces import IFolder
from plone.app.textfield.interfaces import IRichTextValue
from zope import interface


@interface.implementer(ISectionIntro)
class SectionIntro(BrowserView):

    def __call__(self):
        if IFolder.providedBy(self.context):
            self.folder = self.context
            self.text = self.context.Description()
        else:
            self.folder = aq_parent(self.context)
            value = getattr(self.context, 'text', None)
            if value:
                if IRichTextValue.providedBy(value):
                    self.text = value.output
                else:
                    self.text = value
            else:
                self.text = self.context.Description()
        return self.index()