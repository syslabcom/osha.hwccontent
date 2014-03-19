# _+- coding: utf-8 -*-
from five import grok
from osha.hwccontent.mediapartner import IMediaPartner
from osha.hwccontent.browser.organisation import View as OrganisationView
from plone import api
import logging

log = logging.getLogger(__name__)

grok.templatedir("templates")


class View(OrganisationView):
    grok.context(IMediaPartner)
    grok.require('zope2.View')
    grok.template("mediapartner")


class PostAddView(grok.View):
    grok.context(IMediaPartner)

    def render(self):
        properties = api.portal.get_tool('portal_properties')
        fallback = self.context.__parent__.absolute_url()
        url = getattr(
            properties.site_properties,
            'organisation_added_page',
            fallback
        )
        if not url.startswith('http'):
            portal = api.portal.get()
            if url.startswith('/'):
                url = url[1:]
            try:
                obj = portal.restrictedTraverse(url)
                url = obj.absolute_url()
            except:
                log.warn('Could not get feedback page: {0}'.format(url))
                url = fallback
        api.portal.show_message('Profile has been created',
                                request=self.request)
        self.redirect(url)
