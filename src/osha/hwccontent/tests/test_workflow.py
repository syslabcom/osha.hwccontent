import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import helpers

from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestWorkflow(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.organisations = self.portal.get('organisations')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.wftool.setChainForPortalTypes(
            ['osha.hwccontent.organisation'],
            'organisation_workflow')
        self.org = api.content.create(
            self.organisations,
            type='osha.hwccontent.organisation',
            title='Test Organisation',
            id='test-organization')

    def test_reviewer_approves_organization(self):
        helpers.login(self.portal, 'Site Administrator')
        self.wftool.doActionFor(self.org, 'approve_phase_1')
        self.assertEqual(
            self.wftool.getInfoFor(self.org, 'review_state'),
            'approved_phase_1')
