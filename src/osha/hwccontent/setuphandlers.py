import logging
from plone.app.multilingual.browser.setup import SetupMultilingualSite

logger = logging.getLogger('osha.hwccontent')


def setupVarious(context):
    """
    @param context:
    Products.GenericSetup.context.DirectoryImportContext instance
    """

    # We check from our GenericSetup context whether we are running
    # add-on installation for your product or any other proudct
    if context.readDataFile('osha.hwccontent.txt') is None:
        # Not your add-on
        return


def setupMultilingual(context):
    if context.readDataFile('osha.hwccontent.txt') is None:
        return
    portal = context.getSite()

    setupTool = SetupMultilingualSite()
    setupTool.setupSite(portal)

    setupTool.setupSharedFolder()
