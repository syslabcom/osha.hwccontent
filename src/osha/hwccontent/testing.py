from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class OshahwccontentLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import osha.hwccontent
        xmlconfig.file(
            'configure.zcml',
            osha.hwccontent,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'osha.hwccontent:default')

OSHA_HWCCONTENT_FIXTURE = OshahwccontentLayer()
OSHA_HWCCONTENT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(OSHA_HWCCONTENT_FIXTURE,),
    name="OshahwccontentLayer:Integration"
)
OSHA_HWCCONTENT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(OSHA_HWCCONTENT_FIXTURE, z2.ZSERVER_FIXTURE),
    name="OshahwccontentLayer:Functional"
)
