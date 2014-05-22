import unittest2 as unittest
from plone import api
from plone.app.testing import helpers, SITE_OWNER_NAME

from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestHelper(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        helpers.login(self.app, SITE_OWNER_NAME)
        self.org = api.content.create(
            self.portal.get('organisations'),
            type='osha.hwccontent.organisation',
            title='Test Organisation',
            id='test-organisation',
            key_email=u'harold@testorganisation.com',
            key_name=u'Harold van Testinger')
        api.content.transition(self.org, 'approve_phase_1')
        self.hw_view = self.portal.restrictedTraverse('hw_view')

    def tearDown(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        api.content.delete(self.org)

    def test_get_organisations_folder_url(self):
        self.assertEquals(self.hw_view.get_organisations_folder_url(),
                          'http://nohost/plone/organisations')

    def test_get_my_profiles_anonymous(self):
        helpers.logout()
        self.assertEquals(self.hw_view.get_my_profiles(),
                          [])

    def test_get_my_profiles_site_owner(self):
        helpers.login(self.app, SITE_OWNER_NAME)
        self.assertEquals(self.hw_view.get_my_profiles(),
                          [])

    def test_get_my_profiles_applicant(self):
        helpers.login(self.portal, 'harold')
        self.assertEquals(self.hw_view.get_my_profiles(),
                          [{'url': self.org.absolute_url(),
                            'Title': self.org.Title(),
                            'portal_type': self.org.portal_type,
                            'review_state': 'approved_phase_1'}])
