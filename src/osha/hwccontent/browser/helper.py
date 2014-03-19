# -*- coding: utf-8 -*-

from Acquisition import (
    aq_base,
    aq_inner,
)
from Products.CMFPlone.utils import (
    safe_unicode,
    getDefaultPage,
)
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.Five.utilities.interfaces import IMarkerInterfaces
from five import grok
from plone import api
from plone.app.contenttypes.interfaces import IImage
from plone.multilingual.interfaces import (
    ITranslationManager,
    ITranslatable,
)
from zope.interface import implements
from zope.interface import Interface
import logging

from osha.hwccontent import (
    FOP_GROUP_NAME,
    OCP_GROUP_NAME,
)
from osha.hwccontent import utils
from osha.hwccontent.behaviors.moreabout import (
    IRelatedSites,
    ISectionImage,
)

log = logging.getLogger(__name__)

EMAIL_FILTER = [
    "herman.baets@telenet.be",
]


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

    def cropHtmlText(self, text, length, ellipsis=u'...'):
        """ first strip html, then crop """
        context = aq_inner(self.context)
        portal_transforms = getToolByName(context, 'portal_transforms')
        if isinstance(text, unicode):
            text = text.encode('utf-8')
        try:
            text = portal_transforms.convert('html_to_text', text).getData()
            text = text.decode('utf-8')
        except Exception, err:
            log.error(
                'An error occurred in cropHTMLText, original text: %s, '
                'message: %s URL: %s' % (
                    str([text]), str(err), context.absolute_url()
                )
            )
            return text
        return context.restrictedTraverse('@@plone').cropText(
            text, length, ellipsis)

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
        profiles = cat(portal_type=[
            'osha.hwccontent.organisation', 'osha.hwccontent.focalpoint'],
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
                'portal_type': obj.portal_type,
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

    def get_len_translations(self):
        if not ITranslatable.providedBy(self.context):
            return 0
        tm = ITranslationManager(self.context)
        return len(tm.get_translations())


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
        send_email = bool(self.request.get('send_email', False))
        for fp in cat(portal_type=['osha.hwccontent.focalpoint']):
            obj = fp.getObject()
            username, created = utils.create_key_user_if_not_exists(obj)
            if username is not None:
                group = gt.getGroupById(FOP_GROUP_NAME)
                if group is None:
                    gt.addGroup(FOP_GROUP_NAME)
                    group = gt.getGroupById(FOP_GROUP_NAME)
                group.addMember(username)
                self.request.set('is_fop', True)
                self.request.set('name', obj.key_name.encode('utf-8').strip())
                if send_email:
                    rt.mailPassword(username, self.request)
                if created:
                    created_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
                else:
                    existed_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
            else:
                failed.append(u"<a href='{0}'>{1}</a>".format(
                    obj.absolute_url(), safe_unicode(obj.Title())))
        msg = (
            u'<html><p>Send email (enable via send_email=1): {0}'
            u'<h2>Created users:</h2><p>{1}</p>'
            u'<h2>Existing users:</h2><p>{2}</p>'
            u'<h2>Failed profiles:</h2><p>{3}</p></html>'
        ).format(
            send_email,
            u'<br>'.join(created_users),
            u'<br>'.join(existed_users),
            u'<br>'.join(failed)
        )
        return msg


class ResetOCPAccounts(grok.View):
    grok.name('reset-ocp-accounts')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        cat = getToolByName(self.context, 'portal_catalog')
        gt = getToolByName(self.context, 'portal_groups')
        rt = getToolByName(self.context, 'portal_registration')
        created_users = []
        existed_users = []
        failed = []
        for fp in cat(portal_type=['osha.hwccontent.organisation']):
            obj = fp.getObject()
            if len(EMAIL_FILTER) and obj.key_email not in EMAIL_FILTER:
                continue
            username, created = utils.create_key_user_if_not_exists(obj)
            if username is not None:
                group = gt.getGroupById(OCP_GROUP_NAME)
                if group is None:
                    gt.addGroup(OCP_GROUP_NAME)
                    group = gt.getGroupById(OCP_GROUP_NAME)
                group.addMember(username)
                self.request.set('is_ocp', True)
                self.request.set('name', obj.key_name.encode('utf-8'))
                rt.mailPassword(username, self.request)
                if created:
                    created_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
                else:
                    existed_users.append(u"{0} <a href='{1}'>{2}</a>".format(
                        username, obj.absolute_url(), safe_unicode(obj.Title())))
            else:
                failed.append(u"<a href='{0}'>{1}</a>".format(
                    obj.absolute_url(), safe_unicode(obj.Title())))
        msg = (
            u'<html><h2>Created users:</h2><p>{0}</p>'
            u'<h2>Existing users:</h2><p>{1}</p>'
            u'<h2>Failed profiles:</h2><p>{2}</p></html>'
        ).format(
            u'<br>'.join(created_users),
            u'<br>'.join(existed_users),
            u'<br>'.join(failed))
        return msg


class PropagateFolderSettings(grok.View):
    """ This view propagates all settings pertaining to layout to the translations
    """
    grok.name('propagate-folder-settings')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        cat = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type='Folder', Language='en')
        res = cat(query)
        log.info('Total no. of folders found: {0}'.format(len(res)))
        for r in res:
            if r.getPath().split('/')[2] != 'en':
                log.warning("Found a folder with lang EN not under /en: {0}".format(
                    r.getPath()))
                continue
            obj = r.getObject()
            if not ITranslatable.providedBy(obj):
                log.warning('Found a folder that is not translatable, WTF: {0}'.format(
                    r.getPath()))
                continue
            ordering = obj.getOrdering()
            order = ordering.idsInOrder()
            tm = ITranslationManager(obj)
            log.info('Handling folder {0}.'.format('/'.join(obj.getPhysicalPath())))
            for lang, trans in tm.get_translations().items():
                if lang == 'en':
                    continue
                # Copy "Exclude from navigation", section images and related sites
                trans.exclude_from_nav = obj.exclude_from_nav
                IRelatedSites(trans).related_sites_links = IRelatedSites(obj).related_sites_links
                ISectionImage(trans).section_image = ISectionImage(obj).section_image
                # Copy over marker interfaces
                ifaces_to_add = IMarkerInterfaces(obj).getDirectlyProvidedNames()
                if len(ifaces_to_add):
                    t_ifaces = IMarkerInterfaces(trans)
                    add = t_ifaces.dottedToInterfaces(ifaces_to_add)
                    t_ifaces.update(add=add, remove=list())
                # handle the default page settings
                prop = 'default_page'
                propval = aq_base(obj).getProperty(prop, None)
                if propval:
                    # get translation of default-page, if it exists (since the id might be different!)
                    default_page = getattr(obj, propval, None)
                    t_default_page = default_page and ITranslationManager(default_page).get_translation(lang)
                    if not t_default_page:
                        continue
                    # check if marker interfaces need to be copied
                    dp_ifaces_to_add = IMarkerInterfaces(default_page).getDirectlyProvidedNames()
                    if len(dp_ifaces_to_add):
                        t_dp_ifaces = IMarkerInterfaces(t_default_page)
                        add = t_dp_ifaces.dottedToInterfaces(dp_ifaces_to_add)
                        t_dp_ifaces.update(add=add, remove=list())
                    if aq_base(trans).hasProperty(prop):
                        trans._delProperty(prop)
                    trans._setProperty(id=prop, value=t_default_page.id, type="string")
                # now set the correct order
                t_ordering = trans.getOrdering()
                t_order = t_ordering.idsInOrder()
                for i in range(len(order)):
                    if order[i] in t_order:
                        t_ordering.moveObjectToPosition(
                            order[i], i, suppress_events=True)
                if t_order != t_ordering.idsInOrder():
                    trans.reindexObject()

        log.info('Now, fix FOP languages')
        results = cat(portal_type="osha.hwccontent.focalpoint", Language='all')
        fopcnt = 0
        for res in results:
            fop = res.getObject()
            if fop.Language() != '':
                fop.setLanguage('')
                fop.reindexObject()
                fopcnt += 1
        log.info('Reset the language on {0} FOPs'.format(fopcnt))
        return "ok"


class PropagatePageDescriptions(grok.View):
    """ This view propagates page descriptions from default pages to
    their parent folders.
    """
    grok.name('propagate-page-descriptions')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        cat = getToolByName(self.context, 'portal_catalog')
        query = dict(portal_type='Folder', Language='all')
        res = cat(query)
        cnt = 0
        log.info('Total no. of folders found: {0}'.format(len(res)))
        for r in res:
            try:
                obj = r.getObject()
            except:
                log.warn("Stale catalog entry for {0}".format(r.getPath()))
                continue
            if obj.Description() == '':
                default_page = getDefaultPage(obj, self.request)
                if default_page:
                    obj.setDescription(getattr(obj, default_page).Description())
                    obj.reindexObject()
                    cnt += 1
            if cnt % 10 == 0:
                log.info("Handled {0} folders".format(cnt))
        return "Finished settings descriptions, handled a total of {0}".format(cnt)


class CreateAndPopulatePartnersGroup(grok.View):
    grok.name('create-partners-group')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        group = utils.create_and_populate_partners_group()
        return "Group '{0}' created and/or populated.".format(group.getId())


class GetFOPEmails(grok.View):
    """ This view propagates all settings pertaining to layout to the translations
    """
    grok.name('get-fop-emails')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        fops = catalog(portal_type='osha.hwccontent.focalpoint')
        out = ['"FOP name", "Link", "Contact person", "Contact Email"']
        for fop in fops:
            obj = fop.getObject()
            out.append(
                u'"{0}", "{1}", "{2}", "{3}"'.format(
                    obj.title, obj.absolute_url(), obj.key_name, obj.key_email))
        return "\n".join(out)


class GetOCPEmails(grok.View):
    """ This view propagates all settings pertaining to layout to the translations
    """
    grok.name('get-ocp-emails')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    def render(self):
        catalog = getToolByName(self.context, 'portal_catalog')
        fops = catalog(portal_type='osha.hwccontent.organisation')
        out = ['"OCP name", "Link", "Contact person", "Contact Email"']
        for fop in fops:
            obj = fop.getObject()
            out.append(
                u'"{0}", "{1}", "{2}", "{3}"'.format(
                    obj.title, obj.absolute_url(), obj.key_name, obj.key_email))
        return "\n".join(out)
