# -*- coding: utf-8 -*-
from Acquisition import aq_parent
from Products.CMFPlone.utils import getDefaultPage
from osha.hwccontent.interfaces import ITwoImages, ISectionIntro, IFullWidth
from plone.app.layout.globals import layout
from plone.app.layout.navigation.interfaces import INavigationRoot


class LayoutPolicy(layout.LayoutPolicy):

    def is_subsection(self, context, view):
        # if isDefaultPage(context):
        #
        if ISectionIntro.providedBy(context) or ISectionIntro.providedBy(view):
            return False
        while not INavigationRoot.providedBy(context):
            context = aq_parent(context)
            if ISectionIntro.providedBy(context):
                return True
            default_page = getDefaultPage(context, self.request)
            if default_page and ISectionIntro.providedBy(
                    getattr(context, default_page)):
                return True
        return False

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag."""

        body_class = super(LayoutPolicy, self).bodyClass(template, view)

        is_special = False

        # is there a marker interface for 2 images on the context or view?
        if ITwoImages.providedBy(self.context) or ITwoImages.providedBy(view):
            body_class += " two-images"
            is_special = True

        # is there a marker interface for section intro?
        if ISectionIntro.providedBy(self.context) or \
                ISectionIntro.providedBy(view):
            body_class += " section-intro"
            is_special = True

        # is there a marker interface for 2 full width?
        if IFullWidth.providedBy(self.context) or IFullWidth.providedBy(view):
            body_class += " full-width"
            is_special = True

        if not is_special and self.is_subsection(self.context, view):
            body_class += " subsection"

        return body_class
