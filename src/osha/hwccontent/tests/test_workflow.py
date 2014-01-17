# vim: set fileencoding=utf-8 :

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import helpers, SITE_OWNER_NAME

from osha.hwccontent import events
from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestWorkflow(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def _mock_send(self, msg, *args, **kw):
        self.sent_mails.append(msg)

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.portal.email_from_address = 'hwc@hwc.org'
        props = self.portal.portal_properties.site_properties

        self.organisations = self.portal.get('organisations')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.wftool.setChainForPortalTypes(
            ['osha.hwccontent.organisation'],
            'organisation_workflow')

        events._send_emails = False
        self.org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='Test Organisation',
            id='test-organisation',
            key_email=u'harold@testorganisation.com',
            key_name=u'Harold van Testinger')
        if props.getProperty('use_email_as_login'):
            self.creator_id = 'harold@testorganisation.com'
        else:
            self.creator_id = 'harold'

        self.sent_mails = []
        events._send_emails = True
        self.portal.MailHost.send = self._mock_send

    def tearDown(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        if 'test-organisation' in self.organisations.objectIds():
            api.content.delete(self.org)
        api.user.delete(self.creator_id)

    def test_organisation_created(self):
        new_org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='New Organisation',
            id='new-organisation',
            key_email=u'ignatius@neworganisation.com',
            key_name=u'Ignatius Schliefenmühl')
        self.assertEqual(len(self.sent_mails), 2, msg='Mail not sent')
        self.assertIn('ignatius@neworganisation.com',
                      '\n'.join(self.sent_mails))
        self.assertIn(self.portal.email_from_address,
                      '\n'.join(self.sent_mails))
        self.assertIn(new_org.absolute_url(),
                      '\n'.join(self.sent_mails))

    def test_reviewer_approves_organisation(self):
        helpers.login(self.portal, 'Site Administrator')
        self.assertFalse(api.user.get(self.creator_id))
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'approved_phase_1')
        user = api.user.get(self.creator_id)
        self.assertEqual(
            user.getProperty('fullname'),
            'Harold van Testinger')
        self.assertEqual(
            user.getProperty('email'),
            'harold@testorganisation.com')
        self.assertEqual(
            set(self.org.get_local_roles_for_userid(user.getId())),
            set(('Reader', 'Contributor', 'Editor')))
        self.assertNotIn(
            'View',
            [p['name'] for p in self.org.permissionsOfRole('Anonymous')
                if p['selected']])
        self.assertEqual(len(self.sent_mails), 1, msg='Mail not sent')
        self.assertIn('harold@testorganisation.com', self.sent_mails[0])

    def test_creator_cannot_submit_incomplete_organisation(self):
        events._send_emails = False
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        events._send_emails = True

        helpers.login(self.portal, self.creator_id)
        self.assertNotIn(
            'submit',
            [a['id'] for a in self.wftool.listActions(object=self.org)])

    def test_creator_submits_organisation(self):
        events._send_emails = False
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        events._send_emails = True

        helpers.login(self.portal, self.creator_id)
        self.org.mission_statement = u'We Care Because We Can'
        self.assertIn(
            'submit',
            [a['id'] for a in self.wftool.listActions(object=self.org)])
        self.wftool.doActionFor(self.org, 'submit')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'pending_phase_2')
        self.assertEqual(len(self.sent_mails), 2, msg='Mail not sent')
        self.assertIn('harold@testorganisation.com',
                      '\n'.join(self.sent_mails))
        self.assertIn(self.portal.email_from_address,
                      '\n'.join(self.sent_mails))
        self.assertIn(self.org.absolute_url(),
                      '\n'.join(self.sent_mails))

    def test_reviewer_publishes_organisation(self):
        events._send_emails = False
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        self.org.mission_statement = u'We Care Because We Can'
        self.wftool.doActionFor(self.org, 'submit')
        events._send_emails = True

        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'publish')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'published')
        self.assertIn(
            'View',
            [p['name'] for p in self.org.permissionsOfRole('Anonymous')
                if p['selected']])

    def test_reviewer_rejects_organisation(self):
        helpers.login(self.portal, 'Site Administrator')
        self.assertIn(
            'test-organisation',
            self.organisations.objectIds())
        self.org.reject()
        self.assertNotIn(
            'test-organisation',
            self.organisations.objectIds())
        self.assertEqual(len(self.sent_mails), 1, msg='Mail not sent')
        self.assertIn('harold@testorganisation.com', self.sent_mails[0])
        self.assertIn('rejected', self.sent_mails[0])
