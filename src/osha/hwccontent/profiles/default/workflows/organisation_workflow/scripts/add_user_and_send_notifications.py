## Script (Python) "add_user_and_send_notifications"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=
##
import string
import random

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

portal = state_change.getPortal()
obj = state_change.object

data = dict(
    object_url=obj.absolute_url(),
    portal_url=portal.absolute_url(),
    creator_name=obj.key_name,
    creator_email=obj.key_email,
    from_addr=portal.getProperty('email_from_address', ''),
    subject='Profile approved',
)
use_email_as_username = portal.portal_properties.site_properties.use_email_as_login
username = data['creator_email']
if not use_email_as_username:
    username = username.split('@')[0]
data['username'] = username
if portal.portal_membership.getMemberById(username) is None:
    chars = string.ascii_letters + string.digits + '\'()[]{}$%&#+*~.,;:-_'
    password = ''.join(random.choice(chars) for x in range(16))
    while portal.portal_registration.testPasswordValidity(password):
        password = ''.join(random.choice(chars) for x in range(16))
    portal.portal_registration.addMember(
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
    context.MailHost.send(mail_body_tpl.format(**data))
