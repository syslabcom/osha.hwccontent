from zope.i18nmessageid import MessageFactory
from AccessControl import ModuleSecurityInfo

OCP_GROUP_NAME = "Official Campaign Partners"
FOP_GROUP_NAME = "national-focal-points"
MP_GROUP_NAME = 'media-partners'

_ = MessageFactory("osha.hwc")

# OBSOLETE:
# i18n messages that i18nextract misses for some reason can be listed here
# Rather, use manual_translations.py for this


def initialize(context):
    ModuleSecurityInfo('osha.hwccontent.utils').declarePublic(
        'validate_userid_pwreset')
