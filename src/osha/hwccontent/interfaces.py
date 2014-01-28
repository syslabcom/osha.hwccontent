# _+- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import (
    IPloneAppContenttypesLayer, IFolder)
from plone.dexterity.interfaces import IDexterityContent
from plone.event.interfaces import IEventAccessor as IPloneEventAccessor
from zope.interface import Attribute


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


class IMaterialsView(IDexterityContent):
    """Marker interface for materials listing view"""


class IEventAccessor(IPloneEventAccessor):
    """Extend event accessor with our own fields"""

    organiser = Attribute(u"The organiser of the event.")
