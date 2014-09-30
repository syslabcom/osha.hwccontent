# _+- coding: utf-8 -*-
from five import grok
from osha.hwccontent.eguide_storage import IEguideStorage
from plone.directives import dexterity
from plone import api
from zope import component
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

    def get_languages(self):
        ldict = {}
        langtool = api.portal.get_tool('portal_languages')
        for item in self.eguides:
            if not ldict.get(item['language']):
                ldict[item['language']] = \
                        langtool.getNameForLanguageCode(item['language'])
        return ldict

    def get_current_language(self):
        """ @return: Two-letter string, the active language code
        """
        return component.getMultiAdapter(
                (self.context, self.request),
                name=u'plone_portal_state').language()
