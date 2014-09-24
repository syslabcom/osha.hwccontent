# _+- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from five import grok
from plone.directives import dexterity
from osha.hwccontent.eguide_storage import IEguideStorage
import logging

log = logging.getLogger(__name__)

grok.templatedir("templates")


class View(dexterity.DisplayForm):
    grok.context(IEguideStorage)
    grok.require('zope2.View')
    grok.template("eguides")

    @property
    def eguides(self):
        obj = self.context
        eguides = []
        for item in obj.eguides:
            guide = getattr(obj, item['attachment'], None)
            if not guide:
                continue
            item['download'] = guide.absolute_url()
            item['flagname'] = item['country'].lower().replace(" ", "_")
            eguides.append(item)

        return eguides
