# -*- coding: utf-8 -*-
from osha.hwccontent import _
from osha.hwccontent import OrderedDict
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm


COUNTRIES = {
    'AA': 'Pan-European',
    'AT': 'Austria',
    'BE': 'Belgium',
    'BG': 'Bulgaria',
    'CH': 'Switzerland',
    'CY': 'Cyprus',
    'CZ': 'Czech Republic',
    'DE': 'Germany',
    'DK': 'Denmark',
    'EE': 'Estonia',
    'ES': 'Spain',
    'FI': 'Finland',
    'FR': 'France',
    'GB': 'United Kingdom',
    'GR': 'Greece',
    'HR': 'Croatia',
    'HU': 'Hungary',
    'IE': 'Ireland',
    'IS': 'Iceland',
    'IT': 'Italy',
    'LI': 'Liechtenstein',
    'LT': 'Lithuania',
    'LU': 'Luxembourg',
    'LV': 'Latvia',
    'MT': 'Malta',
    'NL': 'Netherlands',
    'NO': 'Norway',
    'PO': 'Poland',
    'PT': 'Portugal',
    'RO': 'Romania',
    'SE': 'Sweden',
    'SI': 'Slovenia',
    'SK': 'Slovakia',
}

ORDERED_COUNTRIES = OrderedDict(sorted(COUNTRIES.items(), key=lambda t: t[0]))

countries = SimpleVocabulary(
    [SimpleTerm(value=name, title=_(name)) for (code, name) in ORDERED_COUNTRIES.items()]
)

countries_with_ids = SimpleVocabulary(
    [SimpleTerm(value=code, title=_(name)) for (code, name) in ORDERED_COUNTRIES.items()])

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


@implementer(IVocabularyFactory)
class LanguagesVocabulary(object):
    """ """

    def __call__(self, context):
        site = getSite()
        plt = getToolByName(site, "portal_languages")
        return SimpleVocabulary(
            [SimpleTerm(value=lang, title=name) for (lang, name) in plt.listSupportedLanguages()])
