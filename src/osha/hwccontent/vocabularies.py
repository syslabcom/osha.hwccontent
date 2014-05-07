from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from osha.hwccontent import _

COUNTRIES = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czech Republic', 'Denmark', 'Estonia', 'Europe', 'Finland',
    'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
    'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Poland',
    'Portugal', 'Romania', 'Slovakia', 'Slovenia',
    'Spain', 'Sweden', 'Switzerland', 'United Kingdom',
]

countries = SimpleVocabulary(
    [SimpleTerm(value=item, title=_(item)) for item in COUNTRIES]
)

ORG_TYPES = [
    'Enterprises', 'Trade unions', 'Employer organisations',
    'OSH professionals', 'Research', 'Other']

organisation_types = SimpleVocabulary(
    [SimpleTerm(value=item, title=_(item)) for item in ORG_TYPES]
)

FOP_ORG_TYPES = [
    'State Agency', 'Labour Inspectorate ', 'Public institution',
    'Government organisation', 'Private Company', 'Public Company',
    'Government body', 'Public Authority']

fop_organisation_types = SimpleVocabulary(
    [SimpleTerm(value=item, title=_(item)) for item in FOP_ORG_TYPES]
)

YES_NO = [
    ("Please select", None),
    ("Yes", True),
    ("No", False),
]

yes_no = SimpleVocabulary(
    [SimpleTerm(value=item[1], title=_(item[0])) for item in YES_NO]
)


MEDIA_TYPES = [
    'Online', 'Print', 'Newsletter', 'Radio', 'TV', 'Other',
]

media_types = SimpleVocabulary(
    [SimpleTerm(value=item, title=item) for item in MEDIA_TYPES])


MEDIA_READERSHIP = [
    'OSH community', 'SMEs', 'Trade', 'Academics', 'Specialists',
    'EU institutions', 'General audience',
]

media_readership = SimpleVocabulary(
    [SimpleTerm(value=item, title=item) for item in MEDIA_READERSHIP])
