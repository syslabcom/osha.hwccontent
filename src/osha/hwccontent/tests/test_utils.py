import unittest2 as unittest
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import helpers, SITE_OWNER_NAME

from osha.hwccontent.utils import (
    create_group_if_not_exists,
    create_and_populate_partners_group,
    create_key_user_if_not_exists,
)
from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestUtils(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.organisations = self.portal.get('organisations')
        self.org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='Test Organisation',
            id='test-organisation',
            key_email=u'harold@testorganisation.com',
            key_name=u'Harold van Testinger')

    def test_create_group_if_not_exists(self):
        create_group_if_not_exists("Test Group 2000")
        pg = getToolByName(self.portal, 'portal_groups')
        self.assertTrue(
            pg.getGroupById("Test Group 2000") is not None)

    def test_create_and_populate_partners_group(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        group = create_and_populate_partners_group()
        self.assertTrue(group is not None)
        self.assertEquals(group.getId(), "Official Campaign Partners")
        self.assertEquals(
            group.getProperty('title'), "Official Campaign Partners")

    def test_create_partners_group_adds_partner_users(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        username, created = create_key_user_if_not_exists(self.org)
        group = create_and_populate_partners_group()
        self.assertIn(username, group.getGroupMemberIds())
