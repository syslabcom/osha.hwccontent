# _+- coding: utf-8 -*-
from five import grok
from osha.hwccontent.mediapartner import IMediaPartner
from osha.hwccontent.browser.organisation import View as OrganisationView

grok.templatedir("templates")


class View(OrganisationView):
    grok.context(IMediaPartner)
    grok.require('zope2.View')
    grok.template("mediapartner")
