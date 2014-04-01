# -*- coding: utf-8 -*-
from osha.hwccontent.browser.resolveuid import uuidToObject
from plone.outputfilters.filters.resolveuid_and_caption import ResolveUIDAndCaptionFilter


"""
Reason for this patch: we need to make the outputfilters that transform saved
text also use out language-aware version of looking up uuids.
"""


def lookup_uid(self, uid):
    return uuidToObject(uid)


ResolveUIDAndCaptionFilter.lookup_uid = lookup_uid
