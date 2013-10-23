from five import grok
from plone.app.contenttypes.content import IFolder, Folder
from plone.app.textfield import RichText

class IOrganisationFolder(IFolder):
    pass

class OrganisationFolder(Folder):
    grok.implements(IOrganisationFolder)

