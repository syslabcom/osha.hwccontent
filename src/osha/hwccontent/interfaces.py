# _+- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from plone.dexterity.interfaces import IDexterityContent


class IOSHAHWCContentLayer(IPloneAppContenttypesLayer):
    """A layer specific to this product. Is registered using browserlayer.xml
    """


class ITwoImages(IDexterityContent):
    """Marker Interface to indicate that a page has 2 horizontal image slots
    """


class ISectionIntro(IDexterityContent):
    """Marker Interface for section intro """
