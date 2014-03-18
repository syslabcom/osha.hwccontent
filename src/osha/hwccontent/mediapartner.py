# _+- coding: utf-8 -*-

from five import grok
from osha.hwccontent import vocabularies
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.interfaces import IAddForm
from zope import schema
from plone import api
from plone.autoform import directives as formdirectives
from plone.directives import (
    dexterity,
    form,
)
from plone.multilingualbehavior import directives
from osha.hwccontent.organisation import (
    EMAIL_HINT_USER,
    EMAIL_HINT_MANAGER,
    IOrganisationBase,
    isEmail,
    _,
)


class IMediaPartner(IOrganisationBase):

    model.fieldset(
        'about_fop',
        label=_(u'About your publication'),
        fields=[
            'title', 'logo', 'country', 'campaign_pledge',
            'publication_type', 'readership',
            'key_name', 'key_position', 'key_email',
            'editor_in_chief', 'url',
            # Social media
            'street', 'address_extra', 'city', 'zip_code', 'phone',
            # 'mission_statement', 'ceo_image',
        ],
    )

    formdirectives.no_omit(IAddForm, 'logo')
    formdirectives.no_omit(IAddForm, 'campaign_pledge')
    formdirectives.no_omit(IAddForm, 'street')
    formdirectives.omitted('fax')
    formdirectives.omitted('campaign_url')
    formdirectives.omitted('street')
    formdirectives.omitted('email')
    formdirectives.omitted('key_phone')

    form.widget(country=CheckBoxFieldWidget)
    country = schema.List(
        title=_(u"Country"),
        description=_(u"Multiple selections are possible"),
        value_type=schema.Choice(
            vocabulary=vocabularies.countries,
        ),
        required=False,
        # min_length=1,
    )
    directives.languageindependent('country')

    form.widget(publication_type=CheckBoxFieldWidget)
    publication_type = schema.List(
        title=_(u"Type of publication"),
        description=_(u"Multiple selections are possible"),
        value_type=schema.Choice(
            vocabulary=vocabularies.media_types,
        )
    )
    directives.languageindependent('publication_type')

    form.widget(readership=CheckBoxFieldWidget)
    readership = schema.List(
        title=_(u"Readership"),
        description=_(u"Multiple selections are possible"),
        value_type=schema.Choice(
            vocabulary=vocabularies.media_readership,
        )
    )
    directives.languageindependent('publication_type')

    key_position = schema.TextLine(
        title=_(u"Position of the main contact person"),
    )
    directives.languageindependent('key_position')

    editor_in_chief = schema.TextLine(
        title=_(u"Editor in Chief"),
    )
    directives.languageindependent('editor_in_chief')


class FormBase(object):

    def adaptWidgets(self):
        self.groups[0].widgets['campaign_pledge'].label = _(
            u"Our contribution")
        self.groups[0].widgets['campaign_pledge'].field.description = _(
            u"Please summarise briefly the support that you will provide "
            u"for this campaign.")
        self.groups[0].widgets['title'].label = _(u'Publication name')
        self.groups[0].widgets['url'].label = _(u"URL")
        self.groups[0].widgets['url'].field.description = u""
        self.groups[0].widgets['logo'].label = _(u"Logo")
        self.groups[0].widgets['logo'].field.description = _(
            u"Please use a format suited for web display if possible (JPEG, "
            u"PNG or GIF).")


class AddForm(dexterity.AddForm, FormBase):
    grok.name('osha.hwccontent.mediapartner')
    grok.context(IMediaPartner)
    grok.require("osha.hwccontent.AddOrganisation")

    def update(self):
        super(AddForm, self).update()
        self.adaptWidgets()


class EditForm(dexterity.EditForm, FormBase):
    grok.context(IMediaPartner)
    grok.require("osha.hwccontent.AddOrganisation")

    def update(self):
        super(EditForm, self).update()
        self.adaptWidgets()

    def updateActions(self):
        """ BEWARE - Dirty Hack (tm)
        uppdateActions() is called _after_ update() in z3c.form.group.GroupForm
        This is important, since we need to manipulate the already set-up
        groups and be sure that our changes don't get overwritten again.
        """
        # Make the key_email field read-only, but only if the user is not a
        # manager
        user = api.user.get_current()
        is_manager = user.checkPermission('Manage portal', self.context)
        for group in self.groups:
            if group.__name__ == 'about_fop':
                email_field = group.fields['key_email'].field
                if is_manager:
                    email_field.description = EMAIL_HINT_MANAGER
                    # Allow changing to an existing email
                    email_field.constraint = isEmail
                else:
                    group.widgets['key_email'].mode = 'display'
                    email_field.description = EMAIL_HINT_USER

        super(EditForm, self).updateActions()
