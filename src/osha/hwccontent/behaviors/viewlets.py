# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from plone.app.layout.viewlets import ViewletBase
from osha.hwccontent.behaviors.moreabout import IRelatedSites, ISeeAlso
from plone.app.layout.navigation.interfaces import INavigationRoot


class SeeAlsoViewlet(ViewletBase):
    """ A simple viewlet which renders see_also """

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
        self.items = [x.to_object for x in self.context.see_also] \
            if self.available else []


class RelatedSitesViewlet(ViewletBase):
    """ A simple viewlet which renders see_also """

    def update(self):
        self.context = IRelatedSites(self.context)
        self.available = True if self.context.related_sites_links else False
