# _+- coding: utf-8 -*-

from datetime import datetime
from json import load
from urllib import urlopen
from urlparse import urljoin

from plone import api
from zope.interface import implements
from Acquisition import aq_parent
from Products.Five.browser import BrowserView

from osha.hwccontent.browser.utils import get_partners, css_by_orientation
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

    def pressreleases(self):
        remote_url = 'http://localhost:8080/osha/portal'
        qurl = urlopen(remote_url + '/jsonfeed?portal_type=PressRelease&path=/de/press/press-releases&subject=stress&language=de')
        for item in load(qurl):
            yield {
                'title': item['title'],
                'releaseDate': datetime.strptime(item['releaseDate'].split('+')[0], '%Y-%m-%dT%H:%M:%S'),
                'url': urljoin(remote_url, item['_path']),
            }
        
        
        
        
    #[u'relatedLinks', u'referenced_content', u'subhead', u'contributors',
     #u'text', u'image', u'creation_date', u'releaseDate', u'imageCaption',
     #u'expirationDate', u'reindexTranslations', u'_image_filename',
     #u'notesToEditors', u'id', u'subject', u'_image_content_type',
     #u'effectiveDate', u'title', u'_text_content_type', u'relatedItems',
     #u'location', u'releaseTiming', u'_seoDescription_content_type',
     #u'excludeFromNav', u'showinsearch', u'_type', u'description',
     #u'searchwords', u'showContacts', u'_searchwords_content_type',
     #u'osha_metadata', u'_rights_content_type', u'_description_content_type',
     #u'modification_date', u'language', u'releaseContacts', u'country',
     #u'rights', u'isNews', u'allowDiscussion', u'seoDescription', u'creators',
     #u'pdfShowTitle', u'_path']

    