from datetime import datetime
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
