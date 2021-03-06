from AccessControl.SecurityManagement import newSecurityManager
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework import RemoteLibraryLayer
from Testing.ZopeTestCase.utils import setupCoreSessions

from plone.testing import z2
from plone import api

from zope.configuration import xmlconfig


class OSHAHWContentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        setupCoreSessions(app)
        # Load ZCML
        import Products.CMFPlacefulWorkflow
        self.loadZCML('configure.zcml', package=Products.CMFPlacefulWorkflow)
        import five.grok
        self.loadZCML('configure.zcml', package=five.grok)

        import osha.hwccontent
        xmlconfig.file(
            'configure.zcml',
            osha.hwccontent,
            context=configurationContext
        )
        # Why not do it like this?
        # self.loadZCML('configure.zcml', package=osha.hwccontent)

        # Apparently the mail template is not grokked properly, registering
        # manually
        xmlconfig.string(
            """<configure xmlns="http://namespaces.zope.org/zope">
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.ApprovePhase1MailTemplate"
                    name="mail_approve_phase_1"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationCreatedCreatorMailTemplate"
                    name="mail_organisation_created_creator"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationCreatedSiteOwnerMailTemplate"
                    name="mail_organisation_created_siteowner"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationSubmittedCreatorMailTemplate"
                    name="mail_organisation_submitted_creator"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationSubmittedSiteOwnerMailTemplate"
                    name="mail_organisation_submitted_siteowner"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationRejectedMailTemplate"
                    name="mail_organisation_rejected"
                    />
                <adapter
                    for="osha.hwccontent.organisation.IOrganisation
                         ZPublisher.HTTPRequest.HTTPRequest"
                    provides="grokcore.view.interfaces.IGrokView"
                    factory="osha.hwccontent.events.OrganisationPublishedCreatorMailTemplate"
                    name="mail_organisation_published_creator"
                    />
               </configure>
            """,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        z2.installProduct(app, 'Products.DateRecurringIndex')

    def tearDownZope(self, app):
        # Uninstall products installed above
        z2.uninstallProduct(app, 'Products.DateRecurringIndex')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'osha.hwccontent:default')
        self.__createDefaultUsers(portal)
        self.__createDefaultContent(portal)

    def __createDefaultUsers(self, portal):
        acl_users = api.portal.get_tool(name='acl_users')

        for role in ('Admin', 'Site Administrator'):
            acl_users.userFolderAddUser( role, 'password', [role], [])

    def __createDefaultContent(self, portal):
        acl_users = api.portal.get_tool(name='acl_users')
        user = acl_users.getUser('Site Administrator')
        newSecurityManager(None, user.__of__(acl_users))
        
        organisations = api.content.create(portal, type='osha.hwccontent.organisationfolder', title='Organisations')
        api.content.transition(organisations, 'publish')
        page = api.content.create(
            organisations,
            type='Document',
            title='Official campaign partners',
        )
        organisations.setDefaultPage(page.getId())
        page.setLayout('document_organisations_view')


class Debugging:
    """This enables the keyword 'start_debugger'
    
    This keyword (by saily) will enter pdb in the console.
    Unsure how useful that is, but I'll let it stay for the moment.
    """

    def start_debugger(self):
        import pdb
        import sys

        for attr in ('stdin', 'stdout', 'stderr'):
            setattr(sys, attr, getattr(sys, '__%s__' % attr))

        pdb.set_trace()

PDB_LIBRARY_FIXTURE = RemoteLibraryLayer(
    bases=(PLONE_FIXTURE, ),
    libraries=(Debugging,),
    name="osha.hwccontent:RobotRemote"
)

OSHA_HWCCONTENT_FIXTURE = OSHAHWContentLayer()
OSHA_HWCCONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OSHA_HWCCONTENT_FIXTURE,),
    name="OSHAHWContentLayer:Integration"
)
OSHA_HWCCONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OSHA_HWCCONTENT_FIXTURE, z2.ZSERVER_FIXTURE, PDB_LIBRARY_FIXTURE),
    name="OSHAHWContentLayer:Functional"
)
