# _+- coding: utf-8 -*-

from five import grok
from osha.hwccontent import _, vocabularies
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from zope import schema
from plone.autoform import directives as formdirectives
from plone.directives import dexterity
from plone.multilingualbehavior import directives
from osha.hwccontent.organisation import IOrganisationBase


class IFocalPoint(IOrganisationBase):

    model.fieldset(
        'about_fop',
        label=_(u'About your Focal Point'),
        fields=[
            'title', 'organisation_type', 'description', 'street',
            'address_extra', 'city', 'zip_code', 'country', 'email', 'phone',
            'fax', 'url', 'campaign_url', 'logo', 'mission_statement',
            'campaign_pledge', 'ceo_image', 'key_name', 'key_email',
            'key_phone',
        ],
    )

    formdirectives.no_omit(IAddForm, 'campaign_pledge')
    formdirectives.no_omit(IAddForm, 'mission_statement')
    formdirectives.no_omit(IAddForm, 'logo')
    formdirectives.no_omit(IAddForm, 'ceo_image')

    description = schema.Text(
        title=_(u'Description'),
    )
    directives.languageindependent('description')

    organisation_type = schema.Choice(
        title=_(u"Organisation type"),
        vocabulary=vocabularies.fop_organisation_types,
    )
    directives.languageindependent('organisation_type')


class FormBase(object):

    def adaptWidgets(self):
        self.groups[0].widgets['campaign_pledge'].label = _(
            u"Campaign pledge")
        self.groups[0].widgets['campaign_pledge'].field.description = _(
            u"Please summarise briefly the support that you will provide "
            u"for this campaign.")
        self.groups[0].widgets['title'].label = _(u'Organisation name')
        self.groups[0].widgets['logo'].label = _(u"Flag image")
        self.groups[0].widgets['logo'].field.description = _(
            u"Please use a format suited for web display if possible (JPEG, "
            u"PNG or GIF).")
        self.groups[0].widgets['ceo_image'].label = _(u"Organisation logo")
        self.groups[0].widgets['mission_statement'].label = _(u"Mandate")
        self.groups[0].widgets['mission_statement'].field.description = u""


class AddForm(dexterity.AddForm, FormBase):
    grok.name('osha.hwccontent.focalpoint')
    grok.context(IFocalPoint)
    grok.require("osha.hwccontent.AddOrganisation")

    def update(self):
        super(AddForm, self).update()
        self.adaptWidgets()


class EditForm(dexterity.EditForm, FormBase):
    grok.context(IFocalPoint)
    grok.require("osha.hwccontent.AddOrganisation")

    def update(self):
        super(EditForm, self).update()
        self.adaptWidgets()
