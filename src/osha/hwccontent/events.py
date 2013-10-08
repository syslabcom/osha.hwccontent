import string
import random

from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from five import grok
from zope.component import getMultiAdapter

from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.interfaces import IOSHAHWCContentLayer


class ApprovePhase1MailTemplate(grok.View):
    """ """
    grok.name('mail_approve_phase_1')
    grok.context(IOrganisation)
    grok.layer(IOSHAHWCContentLayer)
    grok.require('cmf.ReviewPortalContent')

    def __init__(self, context, request):
        super(ApprovePhase1MailTemplate, self).__init__(context, request)
        obj = self.context
        portal = getToolByName(obj, 'portal_url').getPortalObject()
        self.object_url = obj.absolute_url()
        self.portal_url = portal.absolute_url()
        self.creator_name = obj.key_name
        self.creator_email = obj.key_email
        self.from_addr = portal.getProperty('email_from_address', '')
        self.subject = 'Profile approved'

    def render(self, username):
        self.username = username
        self.template = grok.PageTemplateFile(
            'templates/mail_approve_phase_1.pt')
        return self.template.render(self)


def add_user_and_send_notifications(obj):
    portal = getToolByName(obj, 'portal_url').getPortalObject()
    site_props = getToolByName(obj, 'portal_properties').get('site_properties')
    portal_membership = getToolByName(obj, 'portal_membership')
    portal_registration = getToolByName(obj, 'portal_registration')
    use_email_as_username = site_props.use_email_as_login
    creator_name = obj.key_name
    username = creator_email = obj.key_email

    if not use_email_as_username:
        username = username.split('@')[0]
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

    mail_template = getMultiAdapter(
        (obj, obj.REQUEST),
        name="mail_approve_phase_1")
    MailHost = getToolByName(portal, 'MailHost')
    MailHost.send(mail_template.render(username))


@grok.subscribe(IOrganisation, IBeforeTransitionEvent)
def handle_wf_transition(obj, event):
    if event.new_state.id == 'approved_phase_1':
        add_user_and_send_notifications(obj)
