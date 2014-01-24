# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.User import UnrestrictedUser
from Products.CMFCore.utils import getToolByName

from plone.multilingual.interfaces import (
    ILanguageIndependentFieldsManager, ITranslationManager)

from plone.multilingualbehavior.subscriber import LanguageIndependentModifier

"""
Reason for this patch:
It can happen that the current user does not have view permissions on all
translations of the current object. Therefore, use the _restricted_ variant
for trying to fetch a translation.
NOTE: Remove this patch if we update p.a.m, i.e. any version > 1.2.1
"""


def handle_modified(self, content):

    fieldmanager = ILanguageIndependentFieldsManager(content)
    if not fieldmanager.has_independent_fields():
        return

    sm = getSecurityManager()
    try:
        # Do we have permission to sync language independent fields?
        if self.bypass_security_checks():
            # Clone the current user and assign a new editor role to
            # allow edition of all translated objects even if the
            # current user whould not have permission to do that.
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', ['Editor', ], '')

            # Wrap the user in the acquisition context of the portal
            # and finally switch the user to our new editor
            acl_users = getToolByName(content, 'acl_users')
            tmp_user = tmp_user.__of__(acl_users)
            newSecurityManager(None, tmp_user)

        # Copy over all language independent fields
        transmanager = ITranslationManager(content)
        for translation in self.get_all_translations(content):
            # PATCHED CODE HERE
            trans_obj = transmanager.get_restricted_translation(translation)
            if trans_obj:
                if fieldmanager.copy_fields(trans_obj):
                    self.reindex_translation(trans_obj)
            # END PATCHED CODE
    finally:
        # Restore the old security manager
        setSecurityManager(sm)

LanguageIndependentModifier.handle_modified = handle_modified
