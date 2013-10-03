from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from osha.hwccontent import _

COUNTRIES = [
    'Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus',
    'Czech Republic', 'Denmark', 'Estonia', 'Finland',
    'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
    'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Poland',
    'Portugal', 'Romania', 'Slovak Republic', 'Slovenia',
    'Spain', 'Sweden', 'Switzerland', 'United Kingdom'
]

countries = SimpleVocabulary(
    [SimpleTerm(value=item, title=_(item)) for item in COUNTRIES]
)

ORG_TYPES = [
    'Private company', 'Trade union', 'Employer organisation',
    'OSH professional organisation', 'Research organisation', 'Other']

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
