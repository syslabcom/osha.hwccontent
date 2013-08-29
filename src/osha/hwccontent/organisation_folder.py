from Products.CMFCore.utils import getToolByName
from five import grok
from osha.hwccontent import _, vocabularies
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema

from plone.app.contenttypes.content import IFolder, Folder

class IOrganisationFolder(IFolder):
    pass

class OrganisationFolder(Folder):
    grok.implements(IOrganisationFolder)

