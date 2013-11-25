from Products.CMFCore.utils import getToolByName
from plone.outputfilters.browser.resolveuid import ResolveUIDView as BaseView
from plone.outputfilters.browser.resolveuid import getSite
from zExceptions import NotFound

# See also https://github.com/plone/plone.app.multilingual/issues/102

def uuidToURL(uuid):
    """Resolves a UUID to a URL via the UID catalog index.
    """
    site = getSite()
    catalog = getToolByName(site, 'portal_catalog')
    res = catalog.unrestrictedSearchResults(UID=uuid)
    if res:
        plt = getToolByName(site, 'portal_languages')
        # Check if a translation in the requested language exists
        # XXX Could be made optional via a Control Panel setting
        # "Resolve UIDs to translation of target"
        lang = plt.getPreferredLanguage()
        tg = getattr(res[0], 'TranslationGroup', None)
        if res[0].Language != lang and tg:
            t_res = catalog.unrestrictedSearchResults(
                Language=lang, TranslationGroup=tg)
            if t_res:
                return t_res[0].getURL()
        return res[0].getURL()


class ResolveUIDView(BaseView):

    def __call__(self):
        url = uuidToURL(self.uuid)

        if not url:
            # BBB for kupu
            hook = getattr(self.context, 'kupu_resolveuid_hook', None)
            if hook:
                obj = hook(self.uuid)
                if not obj:
                    raise NotFound("The link you followed is broken")
                url = obj.absolute_url()

        if not url:
            raise NotFound("The link you followed is broken")

        if self.subpath:
            url = '/'.join([url] + self.subpath)

        if self.request.QUERY_STRING:
            url += '?' + self.request.QUERY_STRING

        self.request.response.redirect(url, status=301)

        return ''
