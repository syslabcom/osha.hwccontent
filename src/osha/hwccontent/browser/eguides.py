# _+- coding: utf-8 -*-
from five import grok
from osha.hwccontent.interfaces import IFullWidth
from osha.hwccontent.eguide_storage import IEguideStorage
from plone.multilingual.interfaces import ITranslationManager
from plone.directives import dexterity
from plone import api
from zope import component
from zope.interface import implements
import logging

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

log = logging.getLogger(__name__)

grok.templatedir("templates")


class View(dexterity.DisplayForm):
    grok.context(IEguideStorage)
    grok.require('zope2.View')
    grok.template("eguides")
    implements(IFullWidth)

    @property
    def eguides(self):
        obj = self.context
        eguides = []
        if len(obj.eguides) == 0 and obj.Language() != 'en':
            obj = ITranslationManager(obj).get_translation('en')
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
        return OrderedDict(sorted(
            ldict.items(), key=lambda t: t[1].lower()))

    def get_countries(self):
        countries = set()
        for item in self.eguides:
            countries.add(item['country'])
        countries = list(countries)
        countries.sort()
        return countries

    def get_current_language(self):
        """ @return: Two-letter string, the active language code
        """
        return component.getMultiAdapter(
            (self.context, self.request),
            name=u'plone_portal_state').language()
