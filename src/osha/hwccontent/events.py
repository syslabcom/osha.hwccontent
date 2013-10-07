import string
import random

from Products.CMFCore.utils import getToolByName
from Products.DCWorkflow.interfaces import IBeforeTransitionEvent
from five import grok

from osha.hwccontent.organisation import IOrganisation

mail_body_tpl = """From: {from_addr}
To: {creator_email}
Subject: {subject}

Dear {creator_name},

Your organisation profile has been approved. You can set a password for your user account here:

    {portal_url}/mail_password_form?userid={username}

You can then view and complete the profile here:

    {object_url}

Best regards,

The Site Administration
"""


def add_user_and_send_notifications(obj):
    portal = getToolByName(obj, 'portal_url').getPortalObject()
    site_props = getToolByName(obj, 'portal_properties').get('site_properties')
    portal_membership = getToolByName(obj, 'portal_membership')
    portal_registration = getToolByName(obj, 'portal_registration')
    data = dict(
        object_url=obj.absolute_url(),
        portal_url=portal.absolute_url(),
        creator_name=obj.key_name,
        creator_email=obj.key_email,
        from_addr=portal.getProperty('email_from_address', ''),
        subject='Profile approved',
    )
    use_email_as_username = site_props.use_email_as_login
    username = data['creator_email']
    if not use_email_as_username:
        username = username.split('@')[0]
    data['username'] = username
    if portal_membership.getMemberById(username) is None:
        chars = string.ascii_letters + string.digits + '\'()[]{}$%&#+*~.,;:-_'
        password = ''.join(random.choice(chars) for x in range(16))
        while portal_registration.testPasswordValidity(password):
            password = ''.join(random.choice(chars) for x in range(16))
        portal_registration.addMember(
            username,
            password,
            [],
            properties={'email': data['creator_email'],
                        'username': username,
                        'fullname': data['creator_name'],
                        }
        )
    roles = ["Reader", "Contributor", "Editor"]
    obj.manage_setLocalRoles(username, roles)
    if data['from_addr']:
        MailHost = getToolByName(portal, 'MailHost')
        MailHost.send(mail_body_tpl.format(**data))


@grok.subscribe(IOrganisation, IBeforeTransitionEvent)
def handle_wf_transition(obj, event):
    if event.new_state.id == 'approved_phase_1':
        add_user_and_send_notifications(obj)
