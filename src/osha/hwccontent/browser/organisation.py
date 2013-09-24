# _+- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from five import grok
from osha.hwccontent.organisation import IOrganisation

grok.templatedir("templates")


class View(grok.View):
    grok.context(IOrganisation)
    grok.require('zope2.View')
    grok.template("organisation")

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    def get_events(self):
        return [
            x for x in self.context.objectValues()
            if x.portal_type == 'Event']
        # return self.portal_catalog(
        #     portal_type='Event', path=self.context.getPhysicalPath())

    def get_news(self):
        return [
            x for x in self.context.objectValues()
            if x.portal_type == 'News Item']
        # return self.portal_catalog(
        #     portal_type='News Item', path=self.context.getPhysicalPath())

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
