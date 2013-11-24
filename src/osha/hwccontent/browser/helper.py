# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from five import grok
from plone import api
from plone.app.contenttypes.interfaces import IImage
from zope.interface import implements
from zope.interface import Interface
import logging

from osha.hwccontent import utils

log = logging.getLogger(__name__)


def get_path_to_icon(obj=None, content_type=None):
    if IImage.providedBy(obj):
        return None
    if obj is None and content_type is None:
        log.warn('Could not get object: {0}'.format(obj.getPath()))
        return 'unknown.png'
    mtr = api.portal.get_tool(name='mimetypes_registry')
    if obj is not None and content_type is None:
        for mime in mtr.lookup(obj.file.contentType):
            if mime.icon_path:
                return mime.icon_path
    elif content_type is not None:
        for mime in mtr.lookup(content_type):
            if mime.icon_path:
                return mime.icon_path
    return 'application.png'


class IHelperView(Interface):
    """ """

    def break_in_lines():
        """ sets the views on all folders """

    def my_profile_url():
        """ return url to user's profile """


class HelperView(BrowserView):
    """ Helper View to manage the campaign site setup """
    implements(IHelperView)

    def __init__(self, context, request=None):
        self.context = context

    def break_in_lines(self, text, max_width=20):
        """ tries to add a break after a number of chars """
        arr = []
        text = safe_unicode(text)
        while (text != ''):
            if len(text) < max_width:
                arr.append(text)
                text = ''

            space = text.rfind(u' ', 0, max_width)
            if space == -1:
                arr.append(text)
                text = ''

            arr.append(text[:space])
            text = text[space:]

        carr = [x for x in arr if x.strip() != '']

        text = "<br/>".join(carr)
        lines = len(carr)

        return (lines, text)

    def get_my_profiles(self):
        ms = api.portal.get_tool(name='portal_membership')
        cat = api.portal.get_tool(name='portal_catalog')
        wf = api.portal.get_tool('portal_workflow')
        user = ms.getAuthenticatedMember()
        profiles = cat(portal_type='osha.hwccontent.organisation',
                       key_email=user.getProperty('email'),
                       sort_on='modified',
                       sort_order='descending')
        profile_info = []
        for profile in profiles:
            obj = profile.getObject()
            wfstate = wf.getInfoFor(obj, 'review_state')
            profile_info.append({
                'Title': obj.Title(),
                'url': obj.absolute_url(),
                'review_state': wfstate,
            })
        return profile_info

    def my_profile_url(self):
        profiles = self.get_my_profiles()
        if len(profiles) > 0:
            return profiles[0]['url']
        return ''

    def get_organisations_folder_url(self):
        cat = api.portal.get_tool(name='portal_catalog')
        org_folders = cat(portal_type="osha.hwccontent.organisationfolder",
                          sort_on='modified',
                          sort_order='descending')
        if len(org_folders) > 2:
            log.warn('Multiple organisation folders: {0}'.format(
                ', '.join([f.getPath() for f in org_folders])))
        for folder in org_folders:
            obj = folder.getObject()
            # We want the partners folder, not the focal points folder. Is
            # checking the default page the best way to tell them apart?
            page = obj.restrictedTraverse(obj.getDefaultPage())
            if not page.getLayout() == 'document_organisations_view':
                continue
            return obj.absolute_url()
        return None


class CreateFocalpointUsers(grok.View):
    grok.name('create-focalpoint-users')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        cat = getToolByName(self.context, 'portal_catalog')
        gt = getToolByName(self.context, 'portal_groups')
        rt = getToolByName(self.context, 'portal_registration')
        created_users = []
        existed_users = []
        failed = []
        for fp in cat(portal_type=['osha.hwccontent.focalpoint']):
            obj = fp.getObject()
            username, created = utils.create_key_user_if_not_exists(obj)
            if username is not None:
                group = gt.getGroupById("Focal Points")
                if group is None:
                    gt.addGroup("Focal Points")
                    group = gt.getGroupById("Focal Points")
                group.addMember(username)
                if created:
                    rt.mailPassword(username, self.request)
                    created_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
                else:
                    existed_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
            else:
                failed.append(u"<a href='{0}'>{1}</a>".format(
                    obj.absolute_url(), safe_unicode(obj.Title())))
        msg = (u'<html><h2>Created users:</h2><p>{0}</p>'
               u'<h2>Existing users:</h2><p>{1}</p>'
               u'<h2>Failed profiles:</h2><p>{2}</p></html>').format(
                   u'<br>'.join(created_users),
                   u'<br>'.join(existed_users),
                   u'<br>'.join(failed))
        return msg
