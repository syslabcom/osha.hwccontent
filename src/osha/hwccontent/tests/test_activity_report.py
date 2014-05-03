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


class TestActivityReport(unittest.TestCase):

    layer = OSHA_HWCCONTENT_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.qi_tool = getToolByName(self.portal, 'portal_quickinstaller')

    def test_report_times(self):
        """ Make sure that the report only includes changes since last report.
        """
        # The report is protected:
        self.assertRaises(Unauthorized, self.portal.restrictedTraverse, '@@activity-report')
        
        login(self.app, SITE_OWNER_NAME)
        activity_report = self.portal.restrictedTraverse('@@activity-report')
        
        # First make a report that we discard that includes any content already
        # created.
        result = activity_report()
        self.assertGreater(len(result.splitlines()), 1) # More than one line
        
        # Now set the last report date to the future, and make the report
        # again, and make sure it is empty:
        site_properties = api.portal.get_tool('portal_properties').site_properties
        site_properties._setPropValue('last_activity_report', (DateTime()+1).rfc822())

        result = activity_report()
        self.assertEqual(result, 
                         "Partner,Event,Date,URL,Author\r\n") # Only one line, the header
        
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
        #login(self.portal, 'Admin')
        login(self.app, SITE_OWNER_NAME)
        api.content.transition(test_document, 'publish')
        
        activity_report = self.portal.restrictedTraverse('@@activity-report')
        result = activity_report()
        
        # The document:
        self.assertIn(',New Page,', result) # Note that there is no partner
        self.assertIn(',http://nohost/plone/organisations/test_document,Site Administrator', result)
        self.assertIn(',Submit for publication Page,', result)
        self.assertIn(',http://nohost/plone/organisations/test_document,admin', result)
        
        # The organisation:
        self.assertIn('Test Org\xc3\xa4nisation,New Organisation,', result) # Here we have a partner
        self.assertIn(',http://nohost/plone/organisations/test_organisation,Site Administrator', result)
