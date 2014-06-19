# -*- coding: utf-8 -*-
from AccessControl.ZopeGuards import guarded_getattr
from osha.hwccontent.organisation import IOrganisation
from plone.namedfile.scaling import ImageScale


# Trying to circumvent the bug that even authenticated users with edit
# permissions are not allowed to access the scaling, because at this
# stage Plone thinks the user is anon

def validate_access(self):
    if IOrganisation.providedBy(self.context):
        return True

    fieldname = getattr(self.data, 'fieldname',
                        getattr(self, 'fieldname', None))
    guarded_getattr(self.context, fieldname)

ImageScale.validate_access = validate_access
