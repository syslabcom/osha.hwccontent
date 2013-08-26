from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from osha.hwccontent import _

COUNTRIES = [#'Choose yours ...',
        'Austria', 'Belgium', 'Bulgaria', 'Cyprus', 
        'Czech Republic', 'Denmark', 'Estonia', 'Finland', 
        'France', 'Germany', 'Greece', 'Hungary', 'Iceland',
        'Ireland', 'Italy', 'Latvia', 'Liechtenstein', 'Lithuania', 
        'Luxembourg', 'Malta', 'Netherlands', 'Norway', 'Poland', 
        'Portugal', 'Romania', 'Slovak Republic', 'Slovenia', 
        'Spain', 'Sweden', 'Switzerland', 'United Kingdom']

countries = SimpleVocabulary(
    [SimpleTerm(value=item, title=_(item)) for item in COUNTRIES]
    )