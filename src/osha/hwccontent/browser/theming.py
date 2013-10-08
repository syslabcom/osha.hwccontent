# -*- coding: utf-8 -*-
from osha.hwccontent.interfaces import ITwoImages, ISectionIntro
from plone.app.layout.globals import layout


class LayoutPolicy(layout.LayoutPolicy):

    def bodyClass(self, template, view):
        """Returns the CSS class to be used on the body tag."""

        body_class = super(LayoutPolicy, self).bodyClass(template, view)

        # is there a marker interface for 2 images on the context?
        if ITwoImages.providedBy(self.context):
            body_class += " two-images"
        # the marker interface can also be set on the view
        if ITwoImages.providedBy(view):
            body_class += " two-images"

        # is there a marker interface for section intro
        if ISectionIntro.providedBy(self.context):
            body_class += " section-intro"
        # the marker interface can also be set on the view
        if ISectionIntro.providedBy(view):
            body_class += " section-intro"

        return body_class
