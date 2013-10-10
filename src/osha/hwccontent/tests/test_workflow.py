# vim: set fileencoding=utf-8 :

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import helpers, SITE_OWNER_NAME, TEST_USER_ID

from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestWorkflow(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def _mock_send(self, msg):
        self.sent_mails.append(msg)

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal.email_from_address = 'hwc@hwc.org'

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
            key_email=u'harold@testorganisation.com',
            key_name=u'Harold van Testinger')

        self.sent_mails = []
        self.portal.MailHost.send = self._mock_send

    def tearDown(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        api.content.delete(self.org)
        res = self.portal.portal_membership.searchForMembers(
            email='harold@testorganisation.com')
        if res:
            api.user.delete(res[0])

    def test_organisation_created(self):
        new_org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='New Organisation',
            id='new-organization',
            key_email=u'ignatius@neworganisation.com',
            key_name=u'Ignatius Schliefenmühl')
        self.assertEqual(len(self.sent_mails), 2, msg='Mail not sent')
        self.assertIn('To: ignatius@neworganisation.com',
                      '\n'.join(self.sent_mails))
        self.assertIn('To: ' + self.portal.email_from_address,
                      '\n'.join(self.sent_mails))
        self.assertIn(new_org.absolute_url(),
                      '\n'.join(self.sent_mails))

    def test_reviewer_approves_organization(self):
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'approved_phase_1')
        res = self.portal.portal_membership.searchForMembers(
            email='harold@testorganisation.com')
        self.assertEqual(len(res), 1)
        user = res[0]
        self.assertEqual(
            user.getProperty('fullname'),
            'Harold van Testinger')
        self.assertEqual(
            set(self.org.get_local_roles_for_userid(user.getId())),
            set(('Reader', 'Contributor', 'Editor')))
        self.assertNotIn(
            'View',
            [p['name'] for p in self.org.permissionsOfRole('Anonymous')
                if p['selected']])
        self.assertEqual(len(self.sent_mails), 1, msg='Mail not sent')
        self.assertIn('harold@testorganisation.com', self.sent_mails[0])
        self.sent_mails = []

        helpers.login(self.portal, user.getId())
        self.wftool.doActionFor(self.org, 'submit')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'pending_phase_2')
        self.assertEqual(len(self.sent_mails), 2, msg='Mail not sent')
        self.assertIn('To: harold@testorganisation.com',
                      '\n'.join(self.sent_mails))
        self.assertIn('To: ' + self.portal.email_from_address,
                      '\n'.join(self.sent_mails))
        self.assertIn(self.org.absolute_url(),
                      '\n'.join(self.sent_mails))
