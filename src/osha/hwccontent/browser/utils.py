# -*- coding: utf-8 -*-
from Products.CMFCore.interfaces import ISiteRoot
from StringIO import StringIO
from five import grok
from plone import api
from osha.hwccontent import vocabularies

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


def get_partners():
    catalog = api.portal.get_tool(name='portal_catalog')
    results = catalog(
        portal_type="osha.hwccontent.organisation",
        Language='all',
        review_state='published')
    partners = OrderedDict()
    for term in vocabularies.organisation_types:
        partners[term.token] = [[]]

    for result in results:
        try:
            partner = result.getObject()
        except:
            continue
        ot = partner.organisation_type
        if ot not in partners:
            # XXX we should probably log this...
            continue
        # get the last row
        row = partners[ot][-1]
        if len(row) and len(row) % 6 == 0:
            # if the row is "full", create a new one
            partners[ot].append([])
            row = partners[ot][-1]
        row.append(partner)
    return partners


def css_by_orientation(partner):
    """ This is a helper to determine logo orientation for a partner.
    """
    try:
        dim = partner.logo.getImageSize()
    except:
        return 'span2'
    if dim and dim[0] < dim[1]:
        return "span2 logovertical"

    return 'span2'


class PDFContentTypeFixxxer(grok.View):
    """Some PDFs don't have application/pdf as content type. Fixxx this!"""
    grok.name('fix_pdfs')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    content_type = "application/pdf"

    def render(self):
        out = StringIO()
        out.write('Fix PDFs\n\n')
        catalog = api.portal.get_tool(name='portal_catalog')
        results = catalog(portal_type="File", Language="all")
        for res in results:
            obj = res.getObject()
            if obj.file.filename.endswith('pdf'):
                if obj.file.contentType != self.content_type:
                    out.write(
                        'On {url} with filename {name} we had old type'
                        ' {old_type}. Now fixxxed.\n'.format(
                            url=obj.absolute_url(), name=obj.file.filename,
                            old_type=obj.file.contentType))
                    obj.file.contentType = self.content_type
                    obj._p_changed = 1
                    obj.reindexObjex()

        return out.getvalue()
