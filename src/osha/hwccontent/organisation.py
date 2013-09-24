# _+- coding: utf-8 -*-

from osha.hwccontent import _, vocabularies
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from plone.multilingualbehavior import directives


class IOrganisation(model.Schema):

    street = schema.TextLine(
        title = _(u"Street"),
    )
    directives.languageindependent('street')

    address_extra = schema.TextLine(
        required=False,
        title = _(u"Address extra"),
    )
    directives.languageindependent('address_extra')

    city = schema.TextLine(
        title = _(u"City"),
    )
    directives.languageindependent('city')

    zip_code = schema.TextLine(
        title = _(u"Zip code"),
    )
    directives.languageindependent('zip_code')

    country = schema.Choice(
        title = _(u"Country"),
        vocabulary = vocabularies.countries,
    )
    directives.languageindependent('country')

    email = schema.TextLine(
        title = _(u"E-Mail"),
    )
    directives.languageindependent('email')

    phone = schema.TextLine(
        title = _(u"Telephone number"),
    )
    directives.languageindependent('phone')

    fax = schema.TextLine(
        required=False,
        title = _(u"Fax number"),
    )
    directives.languageindependent('fax')

    url = schema.TextLine(
        title = _(u"Website"),
    )
    directives.languageindependent('url')

    campaign_url = schema.TextLine(
        title = _(u"Dedicated Campaign Website"),
    )
    directives.languageindependent('campaign_url')

    logo = NamedBlobImage(
        title = _(u"Company/Organisation logo"),
    )
    directives.languageindependent('logo')

    organisation_type = schema.TextLine(
        title = _(u"Organisation type"),
    )

    business_sector = schema.TextLine(
        title = _(u"Business sector"),
    )

    mission_statement = schema.Text(
        title = _(u"Mission statement"),
    )

    campaign_pledge = schema.Text(
        title = _(u"Our Campaign Pledge"),
    )

    ceo_image = NamedBlobImage(
        title = _(u"Photo of your CEO, President, General Director or other"),
    )
    directives.languageindependent('ceo_image')

    ceo_name = schema.TextLine(
        description = _(u"Name / surname of your CEO, President, General Director or other"),
        title = _(u"CEO"),
    )
    directives.languageindependent('ceo_name')

    ceo_position = schema.TextLine(
        description = _(u"Please indicate the actual position, such as President, General Director, CEO, Chairman, etc"),
        title = _(u"Position identifier"),
    )
    directives.languageindependent('ceo_position')

    key_name = schema.TextLine(
        description = _(u"Name/Surname of main contact person for the Campaign"),
        title = _(u"Contact person"),
    )
    directives.languageindependent('key_name')

    key_position = schema.TextLine(
        title = _(u"Position of the main contact person."),
    )
    directives.languageindependent('key_position')

    key_email = schema.TextLine(
        title = _(u"Email address of main contact person."),
    )
    directives.languageindependent('key_email')

    key_phone = schema.TextLine(
        title = _(u"Telephone number of main contact person."),
    )
    directives.languageindependent('key_phone')

    representative_name = schema.TextLine(
        required=False,
        title = _(u"Name of your organisation\'s health and safety representative"),
    )
    directives.languageindependent('representative_name')

    representative_email = schema.TextLine(
        required=False,
        title = _(u"Email address of your organisation\'s health and safety representative"),
    )
    directives.languageindependent('representative_email')

    representative_phone = schema.TextLine(
        required=False,
        title = _(u"Telephone number of your organisation's health and safety representative"),
    )
    directives.languageindependent('representative_phone')
