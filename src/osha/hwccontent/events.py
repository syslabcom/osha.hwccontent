import string
import random

from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from five import grok
from zope.component import getMultiAdapter
from zope.app.container.interfaces import IObjectAddedEvent

from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.interfaces import IOSHAHWCContentLayer
import logging

log = logging.getLogger(__name__)

_send_emails = True

class MailTemplateBase(grok.View):
    """ """
    grok.baseclass()

    def __init__(self, context, request):
        super(MailTemplateBase, self).__init__(context, request)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        self.object_url = context.absolute_url()
        self.portal_url = portal.absolute_url()
        self.creator_name = context.key_name
        self.creator_email = context.key_email
        self.from_addr = portal.getProperty('email_from_address', '')


class ApprovePhase1MailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_approve_phase_1')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self, username):
        self.username = username
        self.subject = 'Profile approved'
        self.template = grok.PageTemplateFile(
            'templates/mail_approve_phase_1.pt')
        return self.template.render(self)


class OrganisationCreatedCreatorMailTemplate(MailTemplateBase):
    """ """
    grok.name('mail_organisation_created_creator')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def render(self):
        self.subject = 'Profile created'
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
        self.subject = 'Profile created'
        self.template = grok.PageTemplateFile(
            'templates/mail_organisation_created_siteowner.pt')
        if not self.from_addr:
            raise KeyError('email_from_address')
        return self.template.render(self)


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


def _send_notification(obj, template_name, *extra_args):
    if not _send_emails:
        return
    
    mail_template = getMultiAdapter(
        (obj, obj.REQUEST),
        name=template_name)
    MailHost = getToolByName(obj, 'MailHost')
    try:
        MailHost.send(mail_template.render(*extra_args), charset='UTF-8')
    except KeyError as e:
        log.warn('No {0}, cannot send notification {1}'.format(
            str(e), template_name))


def add_user_and_send_notifications(obj):
    site_props = getToolByName(obj, 'portal_properties').get('site_properties')
    portal_membership = getToolByName(obj, 'portal_membership')
    portal_registration = getToolByName(obj, 'portal_registration')
    use_email_as_username = site_props.use_email_as_login
    creator_name = obj.key_name
    username = creator_email = obj.key_email

    if not use_email_as_username:
        username = username.split('@')[0]
    username = username.encode('utf-8')
    if portal_membership.getMemberById(username) is None:
        chars = string.ascii_letters + string.digits + '\'()[]{}$%&#+*~.,;:-_'
        password = ''.join(random.choice(chars) for x in range(16))
        while portal_registration.testPasswordValidity(password):
            password = ''.join(random.choice(chars) for x in range(16))
        portal_registration.addMember(
            username,
            password,
            [],
            properties={'email': creator_email,
                        'username': username,
                        'fullname': creator_name,
                        }
        )
    roles = ["Reader", "Contributor", "Editor"]
    obj.manage_setLocalRoles(username, roles)

    _send_notification(obj, "mail_approve_phase_1", username)


@grok.subscribe(IOrganisation, IBeforeTransitionEvent)
def handle_wf_transition(obj, event):
    if not event.transition:
        return
    if event.transition.id == 'approve_phase_1':
        add_user_and_send_notifications(obj)
    elif event.transition.id == 'submit':
        _send_notification(obj, "mail_organisation_submitted_creator")
        _send_notification(obj, "mail_organisation_submitted_siteowner")


@grok.subscribe(IOrganisation, IObjectAddedEvent)
def handle_organisation_created(obj, event):
    _send_notification(obj, "mail_organisation_created_creator")
    _send_notification(obj, "mail_organisation_created_siteowner")
