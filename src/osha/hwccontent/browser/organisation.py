# _+- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from five import grok
from plone.directives import dexterity
from osha.hwccontent.organisation import IOrganisation

grok.templatedir("templates")


class View(dexterity.DisplayForm):
    grok.context(IOrganisation)
    grok.require('zope2.View')
    grok.template("organisation")

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_events(self):
        results = self.portal_catalog(
            portal_type='plone.app.event.dx.event',
            path='/'.join(self.context.getPhysicalPath()))
        return [x.getObject() for x in results]

    def get_news(self):
        results = self.portal_catalog(
            portal_type='News Item',
            path='/'.join(self.context.getPhysicalPath()))
        return [x.getObject() for x in results]

    def get_news_folder_url(self):
        try:
            return self.context.restrictedTraverse('news').absolute_url()
        except KeyError:
            return ''

    def get_events_folder_url(self):
        try:
            return self.context.restrictedTraverse('events').absolute_url()
        except KeyError:
            return ''


class PostAddView(grok.View):
    grok.context(IOrganisation)

    def render(self):
        url = self.context.__parent__.absolute_url()
        # Add portal message
        self.redirect(url)
