import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import helpers, SITE_OWNER_NAME

from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestWorkflow(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

        def mock_send(msg):
            self.sent_mails.append(msg)
        self.portal.email_from_address = 'hwc@hwc.org'
        self.sent_mails = []
        self.portal.MailHost.send = mock_send

        self.organisations = self.portal.get('organisations')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.wftool.setChainForPortalTypes(
            ['osha.hwccontent.organisation'],
            'organisation_workflow')
        self.org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='Test Organisation',
            id='test-organization',
            key_email='harold@testorganisation.com',
            key_name='Harold van Testinger')

    def tearDown(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        api.content.delete(self.org)
        res = self.portal.portal_membership.searchForMembers(
            email='harold@testorganisation.com')
        if res:
            api.user.delete(res[0])

    def test_reviewer_approves_organization(self):
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'approved_phase_1')
        res = self.portal.portal_membership.searchForMembers(
            email='harold@testorganisation.com')
        self.assertEqual(len(res), 1)
        self.assertEqual(
            res[0].getProperty('fullname'),
            'Harold van Testinger')
        self.assertEqual(
            set(self.org.get_local_roles_for_userid(res[0].getId())),
            set(('Reader', 'Contributor', 'Editor')))
        self.assertNotIn(
            'View',
            [p['name'] for p in self.org.permissionsOfRole('Anonymous')
                if p['selected']])
        self.assertEqual(len(self.sent_mails), 1, msg='Mail not sent')
        self.assertIn('harold@testorganisation.com', self.sent_mails[0])
