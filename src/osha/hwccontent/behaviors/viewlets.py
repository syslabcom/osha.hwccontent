# -*- coding: utf-8 -*-
from plone.app.layout.viewlets import ViewletBase
from osha.hwccontent.behaviors.moreabout import IRelatedSites, ISeeAlso


class SeeAlsoViewlet(ViewletBase):
    """ A simple viewlet which renders see_also """

    def update(self):
        self.context = ISeeAlso(self.context)
        self.available = True if self.context.see_also else False


class RelatedSitesViewlet(ViewletBase):
    """ A simple viewlet which renders see_also """

    def update(self):
        self.context = IRelatedSites(self.context)
        self.available = True if self.context.related_sites_links else False
