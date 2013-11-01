from Products.Five import BrowserView
from plone import api
from zope.interface import implements
from zope.interface import Interface
import logging

log = logging.getLogger(__name__)


class IHelperView(Interface):
    """ """
    
    def break_in_lines():
        """ sets the views on all folders """


class HelperView(BrowserView):
    """ Helper View to manage the campaign site setup """
    implements(IHelperView)

    def __init__(self, context, request=None):
        self.context = context

    def break_in_lines(self, text, max_width=20):
        """ tries to add a break after a number of chars """
        arr = []
        while (text!=''):
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
                'needs_completion': wfstate == 'approved_phase_1',
            })
        return profile_info

    def get_organisations_folder_url(self):
        cat = api.portal.get_tool(name='portal_catalog')
        org_folders = cat(portal_type="osha.hwccontent.organisationfolder",
                          sort_on='modified',
                          sort_order='descending')
        if len(org_folders) > 0:
            if len(org_folders) > 1:
                log.warn('Multiple organisation folders: {0}'.format(
                    ', '.join([f.getPath() for f in org_folders])))
            obj = org_folders[0].getObject()
            return obj.absolute_url()
