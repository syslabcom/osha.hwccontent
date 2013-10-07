# _+- coding: utf-8 -*-
from plone.app.contenttypes.interfaces import IPloneAppContenttypesLayer
from zope.interface import Interface


class IOSHAHWCContentLayer(IPloneAppContenttypesLayer):
    """A layer specific to this product. Is registered using browserlayer.xml
    """


class ITwoImages(Interface):
    """Marker Interface to indicate that a page has 2 horizontal image slots
    """
