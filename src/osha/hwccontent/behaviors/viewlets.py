# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone import api
from plone.app.layout.viewlets import ViewletBase
from osha.hwccontent.behaviors.moreabout import (
    IRelatedSites, ISeeAlso, ISectionImage)
from osha.hwccontent.interfaces import IOrganisationFolder
from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.multilingual.interfaces import (
    ITranslatable, ITranslationManager)


class SeeAlsoViewlet(ViewletBase):
    """ A simple viewlet which renders the 'See also' links """

    def get_datacontext(self, obj):
        if ISeeAlso.providedBy(obj):
            return ISeeAlso(obj)
        if not INavigationRoot.providedBy(obj):
            return self.get_datacontext(aq_parent(obj))
        return None

    def update(self):
        self.context = self.get_datacontext(self.context)
        self.available = True if (self.context and self.context.see_also) \
            else False
        if self.available:
            user = api.user.get_current()
            language = api.portal.get_tool(
                'portal_languages').getPreferredLanguage()
            items = list()
            for relation in self.context.see_also:
                if relation.isBroken():
                    continue
                obj = relation.to_object
                if ITranslatable.providedBy(obj):
                    obj = ITranslationManager(obj).get_restricted_translation(
                        language) or obj
                if user.has_permission('View', obj):
                    items.append(obj)
            self.items = items


class RelatedSitesViewlet(ViewletBase):
    """ A simple viewlet which renders the relates sites links """

    def get_datacontext(self, obj):
        if IRelatedSites.providedBy(obj):
            return IRelatedSites(obj)
        if not INavigationRoot.providedBy(obj):
            return self.get_datacontext(aq_parent(obj))
        return None

    def update(self):
        self.context = self.get_datacontext(self.context)
        self.available = True if (
            self.context and self.context.related_sites_links) else False
        self.items = [x for x in self.context.related_sites_links] \
            if self.available else []


class SectionImageViewlet(ViewletBase):
    """ A simple viewlet that renders the section image(s) """

    def get_datacontext(self, obj):
        if ISectionImage.providedBy(obj):
            return ISectionImage(obj)
        if not IOrganisationFolder.providedBy(obj) \
                and not INavigationRoot.providedBy(obj):
            return self.get_datacontext(aq_parent(obj))
        return None

    def update(self):
        self.context = self.get_datacontext(self.context)
        self.available = True if (
            self.context and self.context.section_image) else False
        self.items = [x.to_object for x in self.context.section_image] \
            if self.available else []
