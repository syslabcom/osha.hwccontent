# _+- coding: utf-8 -*-

from Acquisition import aq_parent
from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from five import grok
from zope.app.container.interfaces import IObjectAddedEvent

from osha.hwccontent import (
    MP_GROUP_NAME,
    OCP_GROUP_NAME,
)
from osha.hwccontent.focalpoint import IFocalPoint
from osha.hwccontent.mediapartner import IMediaPartner
from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.interfaces import IOSHAHWCContentLayer
from osha.hwccontent import utils
from plone.app.contenttypes.interfaces import (
    IEvent,
    INewsItem,
)
from plone.dexterity.interfaces import IDexterityContent
import logging

log = logging.getLogger(__name__)


class MailTemplateBase(grok.View):
    """ """
    grok.baseclass()

    def __init__(self, context, request):
        super(MailTemplateBase, self).__init__(context, request)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.object_url = context.absolute_url()
        self.folder_url = aq_parent(context).absolute_url()
        self.portal_url = portal.absolute_url()
        self.creator_name = context.key_name
        self.organisation_type = getattr(context, 'organisation_type', '')
        self.content_type = context.Type()
        self.creator_email = "%(name)s <%(email)s>" % dict(
            name=context.key_name, email=context.key_email)
        self.from_addr = "%(name)s <%(email)s>" % dict(
            name=portal.getProperty('email_from_name', ''),
            email=portal.getProperty('email_from_address', ''))


class ApprovePhase1MailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_approve_phase_1')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self, username, created):
        self.username = username
        self.subject = 'Profile approved'
        self.template = grok.PageTemplateFile(
            'templates/mail_approve_phase_1.pt')
        self.created = created
        reset_tool = getToolByName(self, 'portal_password_reset')
        membership = getToolByName(self, 'portal_membership')
        member = membership.getMemberById(username)
        self.reset = reset_tool.requestReset(member.getId())
        return self.template.render(self)


class ApproveMediaPartnerMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_approve_media_partner')
    grok.context(IMediaPartner)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self, username, created):
        self.username = username
        self.subject = 'Profile approved'
        self.template = grok.PageTemplateFile(
            'templates/mail_approve_media_partner.pt')
        self.created = created
        reset_tool = getToolByName(self, 'portal_password_reset')
        membership = getToolByName(self, 'portal_membership')
        member = membership.getMemberById(username)
        self.reset = reset_tool.requestReset(member.getId())
        return self.template.render(self)


class OrganisationCreatedCreatorMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_created_creator')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Application to the Healthy Workplaces campaign'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_created_creator.pt')
        return self.template.render(self)


class OrganisationCreatedSiteOwnerMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_created_siteowner')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Application to the Healthy Workplaces campaign'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_created_siteowner.pt')
        if not self.from_addr:
            raise KeyError('email_from_address')
        return self.template.render(self)


class MediapartnerCreatedSiteOwnerMailTemplate(OrganisationCreatedSiteOwnerMailTemplate):
    """ """
    grok.name('mail_mediapartner_created_siteowner')
    grok.context(IMediaPartner)


class OrganisationSubmittedCreatorMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_submitted_creator')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Profile finalised'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_submitted_creator.pt')
        return self.template.render(self)


class OrganisationSubmittedSiteOwnerMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_submitted_siteowner')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Profile submitted'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_submitted_siteowner.pt')
        if not self.from_addr:
            raise KeyError('email_from_address')
        return self.template.render(self)


class OrganisationRejectedMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_rejected')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Profile rejected'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_rejected.pt')
        if not self.from_addr:
            raise KeyError('email_from_address')
        return self.template.render(self)


class MediapartnerRejectedMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_mediapartner_rejected')
    grok.context(IMediaPartner)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Profile rejected'
        self.template = grok.PageTemplateFile('templates/mail_mediapartner_rejected.pt')
        if not self.from_addr:
            raise KeyError('email_from_address')
        return self.template.render(self)


class OrganisationPublishedCreatorMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_published_creator')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Application to the Healthy Workplaces campaign'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_published_creator.pt')
        return self.template.render(self)


class OrganisationContentSubmittedMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_content_submitted')
    grok.context(IDexterityContent)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self, parent):
        self.subject = 'Content submitted'
        self.content_type = self.context.Type()
        self.parent_type = parent.Type()
        self.parent_name = parent.Title()
        self.template = grok.PageTemplateFile(
            'templates/mail_content_submitted.pt')
        return self.template.render(self)


def add_user_and_send_notifications(obj, groupname, template_name):
    username, created = utils.create_key_user_if_not_exists(obj)
    group = utils.create_group_if_not_exists(groupname)
    group.addMember(username)
    utils._send_notification(obj, template_name, username, created)


@grok.subscribe(IOrganisation, IBeforeTransitionEvent)
def handle_wf_transition(obj, event):
    if not event.transition:
        return
    if event.transition.id == 'approve_phase_1':
        add_user_and_send_notifications(obj, OCP_GROUP_NAME, 'mail_approve_phase_1')
    elif event.transition.id == 'submit':
        utils._send_notification(obj, "mail_organisation_submitted_creator")
        utils._send_notification(obj, "mail_organisation_submitted_siteowner")
    elif event.transition.id == 'publish':
        utils._send_notification(obj, 'mail_organisation_published_creator')


@grok.subscribe(IMediaPartner, IBeforeTransitionEvent)
def handle_wf_mp_transition(obj, event):
    if not event.transition:
        return
    elif event.transition.id == 'publish':
        add_user_and_send_notifications(obj, MP_GROUP_NAME, 'mail_approve_media_partner')


@grok.subscribe(IOrganisation, IObjectAddedEvent)
def handle_organisation_created(obj, event):
    utils._send_notification(obj, "mail_organisation_created_creator")
    utils._send_notification(obj, "mail_organisation_created_siteowner")


@grok.subscribe(IMediaPartner, IObjectAddedEvent)
def handle_mediapartner_added(obj, event):
    # utils._send_notification(obj, "mail_organisation_created_creator")
    utils._send_notification(obj, "mail_mediapartner_created_siteowner")


@grok.subscribe(IEvent, IBeforeTransitionEvent)
@grok.subscribe(INewsItem, IBeforeTransitionEvent)
def handle_wf_transition_partners(obj, event):
    if not event.transition:
        return
    if event.transition.id == "submit":
        parent = aq_parent(obj)
        if IOrganisation.providedBy(parent) or IFocalPoint.providedBy(parent):
            utils._send_notification(obj, 'mail_content_submitted', parent)
