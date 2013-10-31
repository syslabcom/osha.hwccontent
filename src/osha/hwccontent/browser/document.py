# _+- coding: utf-8 -*-

from datetime import datetime
from json import load
from urllib import urlopen
from urlparse import urljoin

from plone import api
from zope.interface import implements
from Acquisition import aq_parent
from Products.Five.browser import BrowserView
from plone.app.textfield.interfaces import ITransformer
from plone.app.textfield.value import RichTextValue

from osha.hwccontent.browser.utils import get_partners, css_by_orientation, isotime2dt
from osha.hwccontent.interfaces import IFullWidth

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class FilesView(BrowserView):

    def get_files(self):
        files = [
            x for x in aq_parent(self.context).objectValues()
            if x.portal_type == 'File']
        return files


class OrganisationsView(BrowserView):
    implements(IFullWidth)

    def partners(self):
        return get_partners()

    def css_by_orientation(self, partner):
        """ This is a helper to determine logo orientation for a partner.
        """
        return css_by_orientation(partner)


class FocalPointsView(BrowserView):
    implements(IFullWidth)

    def focalpoints(self):
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(
            portal_type="osha.hwccontent.focalpoint",
            review_state='published')

        letters = {}

        for result in results:
            try:
                fop = result.getObject()
            except:
                continue
            country = fop.country
            letter = country[0].lower()
            if letter not in letters:
                letters[letter] = {}
            letters[letter][country] = fop.absolute_url()
        return letters

class PressReleaseView(BrowserView):
    implements(IFullWidth)

    def remote_url(self):
        properties = api.portal.get_tool('portal_properties')
        return getattr(properties.site_properties, 'osha_json_url', 'https://osha.europa.eu/')
        
    def make_intro(self, item):        
        text = item.get('text')
        if not text:
            return ''

        transformer = ITransformer(self.context)
        value = RichTextValue(text, mimeType=item.get('_text_mime_type', 'text/html'))
        transformedValue = transformer(value, 'text/plain')
        
        if len(transformedValue) < 200:
            return transformedValue
        
        text = transformedValue[:200].rsplit(None, 1)[0]
        return text + u'...'
        
    def pressreleases(self):
        remote_url = self.remote_url()
        lang_tool = api.portal.get_tool("portal_languages")
        lang = lang_tool.getPreferredLanguage()
        subject = self.context.Subject
        qurl = remote_url + '/jsonfeed?portal_type=PressRelease&path=/%s/press/press-releases&Subject=%s&Language=%s' % (lang, ','.join(subject()), lang)

        for item in load(urlopen(qurl)):
            yield {
                'title': item['title'],
                'releaseDate': isotime2dt(item['releaseDate']),
                'url': item['_url'],
                'text': self.make_intro(item)
            }
        
    
    