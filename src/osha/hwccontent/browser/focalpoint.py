# _+- coding: utf-8 -*-
from five import grok
from osha.hwccontent.focalpoint import IFocalPoint
from osha.hwccontent.browser.organisation import View as OrganisationView

grok.templatedir("templates")


class View(OrganisationView):
    grok.context(IFocalPoint)
    grok.require('zope2.View')
    grok.template("focalpoint")
