import string
import random

from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite


def create_key_user_if_not_exists(obj):
    if obj is None:
        obj = getSite()
    site_props = getToolByName(
        obj, 'portal_properties').get('site_properties')
    portal_membership = getToolByName(obj, 'portal_membership')
    portal_registration = getToolByName(obj, 'portal_registration')
    use_email_as_username = site_props.use_email_as_login
    created = False

    username = email = obj.key_email
    if not use_email_as_username:
        username = username.split('@')[0]
    username = username.encode('utf-8')
    if portal_membership.getMemberById(username) is None:
        chars = string.ascii_letters + string.digits + '\'()[]{}$%&#+*~.,;:-_'
        password = ''.join(random.choice(chars) for x in range(16))
        while portal_registration.testPasswordValidity(password):
            password = ''.join(random.choice(chars) for x in range(16))
        fullname = obj.key_name
        portal_registration.addMember(
            username,
            password,
            [],
            properties={'email': email,
                        'username': username,
                        'fullname': fullname,
                        }
        )
        created = True
    roles = ["Reader", "Contributor", "Editor"]
    obj.manage_setLocalRoles(username, roles)
    return username, created
