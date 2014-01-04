import string
import random

from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite

import logging
log = logging.getLogger(__name__)


def create_key_user_if_not_exists(obj):
    if obj is None:
        obj = getSite()
    site_props = getToolByName(
        obj, 'portal_properties').get('site_properties')
    portal_membership = getToolByName(obj, 'portal_membership')
    portal_registration = getToolByName(obj, 'portal_registration')
    plone_utils = getToolByName(obj, 'plone_utils')
    use_email_as_username = site_props.use_email_as_login
    created = False

    username = email = obj.key_email
    if not use_email_as_username:
        username = username.split('@')[0]
    username = username.encode('utf-8')
    if portal_membership.getMemberById(username) is None:
        if portal_registration.isMemberIdAllowed(username) and \
                plone_utils.validateSingleEmailAddress(email):
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
        else:
            log.error(
                'Cannot create account for context %(url)s, username is not '
                'valid: "%(name)s"' % dict(url=obj.absolute_url(), name=username))
            return None, created
    roles = ["Reader", "Contributor", "Editor"]
    obj.manage_setLocalRoles(username, roles)
    return username, created


def create_group_if_not_exists(group_id):
    portal = getSite()
    pg = getToolByName(portal, 'portal_groups')
    group = pg.getGroupById(group_id)
    if group is None:
        pg.addGroup(group_id)
        group = pg.getGroupById(group_id)
    group.setGroupProperties({'title':  group_id})
    return group


def create_and_populate_partners_group():
    portal = getSite()
    group = create_group_if_not_exists("Official Campaign Partners")
    cat = getToolByName(portal, 'portal_catalog')
    orgas = cat(portal_type=['osha.hwccontent.organisation'])
    for orga in orgas:
        username, created = create_key_user_if_not_exists(orga.getObject())
        group.addMember(username)
    return group
