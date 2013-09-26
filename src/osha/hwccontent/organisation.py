# _+- coding: utf-8 -*-

from osha.hwccontent import _, vocabularies
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema
from plone.multilingualbehavior import directives

from plone.directives import dexterity
from plone.directives import form


class IOrganisationPhase1(model.Schema):

    # Countries of Activity
    form.fieldset(
        'about_organisation',
        label=_(u'About your organisation'),
        fields=[
            'countries', 'additional_countries', 'title', 'organisation_type',
            'business_sector', 'social_dialogue', 'street', 'address_extra',
            'city', 'zip_code', 'country', 'email', 'phone', 'fax', 'key_name',
            'key_position', 'key_email', 'key_phone', 'url', 'campaign_url',
        ],
    )

    countries = schema.List(
        title=_(u"Countries of activity"),
        description=_(
            u"Only Pan-European or international organisations / "
            "companies are eligible for the European Campaign Partnership; "
            "please indicate the countries your company is represented through"
            " branches / representative offices / network members"),
        value_type=schema.Choice(
            vocabulary=vocabularies.countries,
        ),
    )
    directives.languageindependent('countries')

    additional_countries = schema.Text(
        title=_(u"Other countries"),
        description=_(
            u"Other countries in which you organisation is represented (enter "
            "names)"),
        required=False,
    )
    directives.languageindependent('additional_countries')

    # Organisation's profile and contact details

    title = schema.TextLine(
        title=_(u"Company / Organisation name")
    )

    organisation_type = schema.Choice(
        title=_(u"Organisation type"),
        vocabulary=vocabularies.organisation_types,
    )
    directives.languageindependent('organisation_type')

    business_sector = schema.TextLine(
        title=_(u"Business sector"),
        description=_(u"Business sector in which you operate"),
    )
    directives.languageindependent('business_sector')

    social_dialogue = schema.Choice(
        title=_(u"Social Dialogue Partner?"),
        description=_(
            u"Are you a Social Partner within the framework of the European "
            "Social Dialogue?"),
        vocabulary=vocabularies.yes_no,
    )

    street = schema.TextLine(
        title=_(u"Address"),
        description=_(u"Street or PO-box")
    )
    directives.languageindependent('street')

    address_extra = schema.TextLine(
        title=_(u"Address extra"),
        required=False,
    )
    directives.languageindependent('address_extra')

    city = schema.TextLine(
        title=_(u"City"),
    )
    directives.languageindependent('city')

    zip_code = schema.TextLine(
        title=_(u"Zip code"),
    )
    directives.languageindependent('zip_code')

    country = schema.TextLine(
        title=_(u"County"),
    )
    directives.languageindependent('country')

    email = schema.TextLine(
        title=_(u"General company email address"),
    )
    directives.languageindependent('email')

    phone = schema.TextLine(
        title=_(u"General telephone number"),
    )
    directives.languageindependent('phone')

    fax = schema.TextLine(
        required=False,
        title=_(u"General fax number"),
    )
    directives.languageindependent('fax')

    # Organisation's contact person

    key_name = schema.TextLine(
        description=_(u"Name/Surname of main contact person for the Campaign"),
        title=_(u"Contact person"),
    )
    directives.languageindependent('key_name')

    key_position = schema.TextLine(
        title=_(u"Position of the main contact person."),
    )
    directives.languageindependent('key_position')

    key_email = schema.TextLine(
        title=_(u"Email address of main contact person."),
    )
    directives.languageindependent('key_email')

    key_phone = schema.TextLine(
        title=_(u"Telephone number of main contact person."),
    )
    directives.languageindependent('key_phone')

    # Organisation's website

    url = schema.TextLine(
        title=_(u"Home page"),
        description=_("Organisation's website"),
    )
    directives.languageindependent('url')

    campaign_url = schema.TextLine(
        title=_(u"Dedicated Campaign Website"),
        description=_(
            u'Special web section dealing with issues related to occupational '
            'health and safety'),
        required=False,
    )
    directives.languageindependent('campaign_url')

    # About your involvement in the Campaign
    form.fieldset(
        'campaign_involvement',
        label=_(u"About your involvement in the campaign"),
        fields=[
            'why_partner', 'promotion_electronic',
            'conferences_check', 'conferences_description',
            'training_check', 'training_description',
            'partnerships_check', 'partnerships_description',
            'promotion_check', 'promotion_description',
            'bestpractice_check', 'bestpractice_description',
            'otheractivities_check', 'otheractivities_description',
        ]
    )

    why_partner = schema.Text(
        title=_(
            u"1. Why do you want to be an official partner of the Healthy "
            u"Workplaces Campaign 2014-15 on ‘Healthy workplaces manage "
            u"stress’?"),
        description=_(u"Please explain briefly"),
    )
    directives.languageindependent('why_partner')

    promotion_electronic = schema.Text(
        title=_(
            u"2. How do you plan to promote and support the Campaign via your "
            "corporate website and in any other electronic means (intranet, "
            "newsletter, social media, etc.)?"),
        description=_(u"Please describe"),
        required=False,
    )
    directives.languageindependent('promotion_electronic')

    conferences_check = schema.Bool(
        title=_(
            u"Conferences, seminars or workshops exclusively or partly "
            "dedicated to the topic of the Campaign"),
        required=False,
    )
    directives.languageindependent('conferences_check')

    conferences_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on topic, main objectives, "
            "profile of participants, etc."),
        required=False,
    )
    directives.languageindependent('conferences_description')

    training_check = schema.Bool(
        title=_(u'Training sessions'),
        required=False,
    )
    directives.languageindependent('training_check')

    training_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on topic, main objectives, "
            "profile of participants, etc."),
        required=False,
    )
    directives.languageindependent('training_description')

    partnerships_check = schema.Bool(
        title=_(
            u"Partnerships with other organisations and schools / colleges / "
            "training centres"),
        required=False,
    )
    directives.languageindependent('partnerships_check')

    partnerships_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on planned activities"),
        required=False,
    )
    directives.languageindependent('partnerships_description')

    promotion_check = schema.Bool(
        title=_(
            u"Promotion in the media (press release, press conference, "
            "advertorials, etc )"),
        required=False,
    )
    directives.languageindependent('promotion_check')

    promotion_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on planned activities"),
        required=False,
    )
    directives.languageindependent('promotion_description')

    bestpractice_check = schema.Bool(
        title=_(u"Best Practice competition / activities"),
        required=False,
    )
    directives.languageindependent('bestpractice_check')

    bestpractice_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on planned activities"),
        required=False,
    )
    directives.languageindependent('bestpractice_description')

    otheractivities_check = schema.Bool(
        title=_(u"Other activities"),
        required=False,
    )
    directives.languageindependent('otheractivities_check')

    otheractivities_description = schema.Text(
        title=_(u"Please describe"),
        description=_(
            u"Please provide some information on planned activities"),
        required=False,
    )
    directives.languageindependent('otheractivities_description')


class IOrganisationPhase2(model.Schema):

    form.fieldset(
        'additional_information',
        label=_(u"Additional information"),
        fields=[
            'mission_statement', 'ceo_name', 'ceo_position', 'ceo_quote',
            'representative_name', 'representative_email',
            'representative_phone', 'logo', 'ceo_image', 'campaign_pledge']
    )

    mission_statement = schema.Text(
        title=_(u"Your mission statement"),
        description=_(u"Briefly outline the mission of your company"),
    )
    directives.languageindependent('mission_statement')

    ceo_name = schema.TextLine(
        title=_(u"CEO"),
        description=_(
            u"Name / surname of your CEO, President, General Director or "
            "other"),
    )
    directives.languageindependent('ceo_name')

    ceo_position = schema.TextLine(
        title=_(u"Position identifier"),
        description=_(
            u"Please indicate the actual position, such as President, General "
            "Director, CEO, Chairman, etc"),
        default=u"CEO",
    )
    directives.languageindependent('ceo_position')

    ceo_quote = schema.TextLine(
        title=_(
            u'His / her quote on the Healthy Workplaces Campaign on "Working '
            'together for risk prevention"'),
    )
    directives.languageindependent('ceo_quote')

    representative_name = schema.TextLine(
        required=False,
        title=_(
            u"Name of your organisation's health and safety representative"),
    )
    directives.languageindependent('representative_name')

    representative_email = schema.TextLine(
        required=False,
        title=_(
            u"Email address of your organisation's health and safety "
            "representative"),
    )
    directives.languageindependent('representative_email')

    representative_phone = schema.TextLine(
        required=False,
        title=_(
            u"Telephone number of your organisation's health and safety "
            "representative"),
    )
    directives.languageindependent('representative_phone')

    logo = NamedBlobImage(
        title=_(u"Company / Organisation logo"),
        description=_(
            u"Please add an image with the company / organisation logo. "
            u"Please use a format suited for web display if possible (JPEG, "
            u"PNG or GIF).")
    )
    directives.languageindependent('logo')

    ceo_image = NamedBlobImage(
        title=_(u"Photo of your CEO, President, General Director or other"),
    )
    directives.languageindependent('ceo_image')

    campaign_pledge = schema.Text(
        title=_(
            u"How does your organisation plan to contribute to making this "
            u"Campaign a joint success? (your Campaign pledge)"),
        description=_(
            u"Please summarise briefly the support that you will provide "
            u"described under STEP 2 of this application form (max. 150 "
            u"words)."),
    )


class IOrganisation(IOrganisationPhase1):
    pass
