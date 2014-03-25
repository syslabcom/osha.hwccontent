# -*- coding: utf-8 -*-
# from Products.CMFCore.utils import getToolByName
from plone import api
from plone.app.contenttypes.browser.album_view import AlbumView
from plone.multilingual.interfaces import ITranslationManager


class HWAlbumView(AlbumView):

    def getAlbumContent(self,
                        container=None,
                        images=0,
                        folders=0,
                        subimages=0,
                        others=0):
        """ Mostly ripped out from atctListAlbum.py
        """
        if not container:
            container = self.context

        # language fallback
        default_lang = api.portal.get_tool(
            "portal_languages").getDefaultLanguage()
        if container.Language() != default_lang:
            container = ITranslationManager(container).get_translation(default_lang)

        contents = container.objectValues()

        result = {}

        if images:
            result['images'] = [x for x in contents if x.portal_type == 'Image']

        if folders:
            result['folders'] = [x for x in contents if x.portal_type == 'Folder']

        if subimages:
            # in this case, container is a sub-folder of the main photo gallery
            result['subimages'] = [x for x in contents if x.portal_type == 'Image']

        # if others:
        #     utils = getToolByName(self.context, 'plone_utils')
        #     searchContentTypes = utils.getUserFriendlyTypes()
        #     filtered = [p_type for p_type in searchContentTypes
        #                 if p_type not in ('Image', 'Folder',)]
        #     if filtered:
        #         # We don't need the full objects for the folder_listing
        #         result['others'] = container.getFolderContents(
        #             {'portal_type': filtered})
        #     else:
        #         result['others'] = ()

        result['others'] = ()
        return result
