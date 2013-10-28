# _+- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import (
    IPloneAppContenttypesLayer, IFolder)
from plone.dexterity.interfaces import IDexterityContent


class IOrganisationFolder(IFolder):
    """ Marker interface for Organisation IOrganisationFolder
    """


class IOSHAHWCContentLayer(IPloneAppContenttypesLayer):
    """A layer specific to this product. Is registered using browserlayer.xml
    """


class IFullWidth(IDexterityContent):
    """Marker Interface to indicate that a page uses full-width layout
    """


class ITwoImages(IDexterityContent):
    """Marker Interface to indicate that a page has 2 horizontal image slots
    """


class ISectionIntro(IDexterityContent):
    """Marker Interface for section intro """
