# _+- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from five import grok
from plone import api
from plone.app.layout.viewlets import ViewletBase
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


class OrganisationManage(ViewletBase):
    """ Manage organisation (OCP) in the themed site """

    def update(self):
        # get user etc
        user = api.user.get_current()
        self.reviewer = user.checkPermission(
            'Review portal content', self.context)
        self.editor = user.checkPermission(
            'Modify portal content', self.context)
        workflow = api.portal.get_tool('portal_workflow')
        self.wfactions = workflow.listActions(object=self.context)
        self.submiturl = None
        for wfaction in self.wfactions:
            if wfaction['id'] == 'submit':
                self.submiturl = wfaction['url']
        self.wfstate = workflow.getInfoFor(self.context, 'review_state')
        self.owner = self.context.email == getattr(user, 'id', '---')

        self.available = True if (self.reviewer or self.editor or self.owner) \
            else False
