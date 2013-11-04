from Products.CMFCore.interfaces import IFolderish
from osha.hwccontent.interfaces import IMaterialsView
from five import grok
from plone import api
from zope import interface

import logging

log = logging.getLogger(__name__)
grok.templatedir('templates')


@interface.implementer(IMaterialsView)
class MaterialsView(grok.View):
    grok.name('folder_materials_view')
    grok.context(IFolderish)
    grok.template('folder_materials_view')

    def get_icon_path(self, obj):
        if obj is None:
            log.warn('Could not get object: {0}'.format(obj.getPath()))
            return 'unknown.png'
        mtr = api.portal.get_tool(name='mimetypes_registry')
        for mime in mtr.lookup(obj.file.contentType):
            if mime.icon_path:
                return mime.icon_path
        return 'application.png'
