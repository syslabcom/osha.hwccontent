from five import grok

from plone.app.contenttypes.content import IFolder, Folder

class IOrganisationFolder(IFolder):
    pass

class OrganisationFolder(Folder):
    grok.implements(IOrganisationFolder)

