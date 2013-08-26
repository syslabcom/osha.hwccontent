from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.robotframework import RemoteLibraryLayer, AutoLogin
from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

from plone.testing import z2

from zope.configuration import xmlconfig


class OSHAHWContentLayer(PloneSandboxLayer):

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
    libraries=(AutoLogin, Debugging,),
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
