from DateTime import DateTime
from datetime import datetime, timedelta
import unittest2 as unittest
from AccessControl import Unauthorized
from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.testing import SITE_OWNER_NAME, TEST_USER_NAME
from plone.app.testing import login, logout

from osha.hwccontent.testing import \
    OSHA_HWCCONTENT_INTEGRATION_TESTING


class TestPartnerReport(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_report_output(self):
        # Set up a default workflow
        wftool = api.portal.get_tool('portal_workflow')
        wftool.setDefaultChain('plone_workflow')

        # Create some documents and test it.
        login(self.portal, 'Site Administrator')
        test_document = api.content.create(container=self.portal.organisations,
                                           type='Document', id='test_document', 
                                           title=u'Test D\xf6cument')
        test_organisation = api.content.create(container=self.portal.organisations,
                                               type='osha.hwccontent.organisation', 
                                               id='test_organisation', 
                                               title=u'Test Org\xe4nisation')
        
        api.content.transition(test_document, 'submit')
        login(self.app, SITE_OWNER_NAME)
        api.content.transition(test_document, 'publish')
        
        activity_report = self.portal.restrictedTraverse('@@organisation-focalpoint-report')
        result = activity_report()
        self.assertIn('Test Org\xe4nisation', result) # Here we have a partner
        