from zope.i18nmessageid import MessageFactory
from AccessControl import ModuleSecurityInfo

OCP_GROUP_NAME = "Official Campaign Partners"
FOP_GROUP_NAME = "national-focal-points"
MP_GROUP_NAME = 'media-partners'

_ = MessageFactory("osha.hwc")

# OBSOLETE:
# i18n messages that i18nextract misses for some reason can be listed here
# Rather, use manual_translations.py for this

# import monkey patches to make sure they are active
import patch_event
import patch_namedfil
import patch_pam


def initialize(context):
    ModuleSecurityInfo('osha.hwccontent.utils').declarePublic(
        'validate_userid_pwreset')
