import logging
from plone.app.multilingual.browser.setup import SetupMultilingualSite
from plone import api

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
    site = api.portal.get()
    add_catalog_indexes(site)


def setupMultilingual(context):
    if context.readDataFile('osha.hwccontent.txt') is None:
        return
    portal = context.getSite()

    setupTool = SetupMultilingualSite()
    setupTool.setupSite(portal)

    setupTool.setupSharedFolder()


def add_catalog_indexes(context):
    '''Add index 'language' to portal_catalog and uid_catalog
    '''
    catalog = api.portal.get_tool('portal_catalog')
    indexes = catalog.indexes()
    schema = catalog.schema()
    wanted = (('organisation_type', 'FieldIndex'), )

    indexables = []
    metadata = []
    for (name, meta_type) in wanted:
        if meta_type and name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info('Added %s for field %s.', meta_type, name)
        if name not in schema:
            catalog.addColumn(name)
            metadata.append(name)
            logger.info('Added catalog metadata column for field %s.' % name)
    if len(indexables) > 0 or len(metadata) > 0:
        logger.info('Indexing new indexes %s.', ', '.join(indexables))
        # We don't call catalog.manage_reindexIndex(ids=indexables)
        # because that method will not update the metadata.
        # Therefore the code of manage_reindexIndex is copied below, but
        # update_metadata is set to True
        paths = catalog._catalog.uids.keys()
        for p in paths:
            obj = catalog.resolve_path(p)
            if obj is None:
                obj = catalog.resolve_url(p, context.REQUEST)
            if obj is None:
                logger.error(
                    'reindexIndex could not resolve an object from the uid '
                    '%r.' % p)
            else:
                # Here we explicitly want to also update the metadata
                catalog.catalog_object(
                    obj, p, idxs=indexables, update_metadata=1)
