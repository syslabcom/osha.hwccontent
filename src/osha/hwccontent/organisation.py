# _+- coding: utf-8 -*-

import re
from Products.validation.validators.BaseValidators import EMAIL_RE
from five import grok
from osha.hwccontent import _, vocabularies
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from z3c.form import field
from z3c.form.interfaces import IAddForm, IEditForm
from zope import schema
from plone.app.textfield import RichText
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives as formdirectives
from plone.directives import dexterity
from plone.multilingualbehavior import directives


INTRO_TEXT_PHASE_1 = _(
    u"<p>Please fill in the form to apply to become an Official Campaign "
    u"Partner (OCP) of the Healthy Workplaces Campaign 2014-15 on "
    u"‘Healthy workplaces manage stress’. Required fields are marked "
    u"with a red dot.</p><p>You might want to take a look at the OCP of "
    u"the 2012-13 Healthy workplaces campaign: "
    u"<a href='http://www.healthy-workplaces.eu/en/about/campaign-partners'>"
    u"http://www.healthy-workplaces.eu/en/about/campaign-partners</a></p><p>"
    u"You might want to download the pdf version of the application "
    u"form. However, only online applications will be evaluated.</p><p>"
    u"Please note that the form consists of two pages.</p>"
)


INTRO_TEXT_PHASE_2 = _(
    u"<p><em>Your application as campaign partner of the Healthy Workplaces "
    u"Campaign 2014-15 on ‘Healthy workplaces manage stress’ has been accepted"
    u"!</em></p><p><em>Please complete now your online profile with some "
    u"additional information. Your online profile will be published on the "
    u"Healthy Workplaces Campaign website (see the partners’ profiles of the "
    u"Healthy Workplaces Campaign 2012-13 <a href='"
    u"http://www.healthy-workplaces.eu/en/about/campaign-partners'>"
    u"http://www.healthy-workplaces.eu/en/about/campaign-partners</a></em></p>"
)


class InvalidEmailError(schema.ValidationError):
    __doc__ = u'Please enter a valid e-mail address.'


def isEmail(value):
    if re.match('^' + EMAIL_RE, value):
        return True
    raise InvalidEmailError


class IOrganisationBase(model.Schema):

    title = schema.TextLine(
        title=_(u"Company / Organisation name")
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

    country = schema.Choice(
        title=_(u"County"),
        vocabulary=vocabularies.countries,
    )
    directives.languageindependent('country')

    email = schema.TextLine(
        title=_(u"General email address"),
        constraint=isEmail,
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

    key_email = schema.TextLine(
        title=_(u"Email address of main contact person."),
        constraint=isEmail,
    )
    directives.languageindependent('key_email')

    key_phone = schema.TextLine(
        title=_(u"Telephone number of main contact person."),
    )
    directives.languageindependent('key_phone')

    # Organisation's website

    url = schema.URI(
        title=_(u"Home page"),
        description=_("Organisation's website"),
    )
    directives.languageindependent('url')

    campaign_url = schema.URI(
        title=_(u"Dedicated Campaign Website"),
        description=_(
            u'Special web section dealing with issues related to occupational '
            'health and safety'),
        required=False,
    )
    directives.languageindependent('campaign_url')

    campaign_pledge = RichText(
        title=_(
            u"How does your organisation plan to contribute to making this "
            u"Campaign a joint success? (your Campaign pledge)"),
        description=_(
            u"Please summarise briefly the support that you will provide "
            u"described under STEP 2 of this application form (max. 150 "
            u"words)."),
    )
    directives.languageindependent('campaign_pledge')
    formdirectives.omitted('campaign_pledge')
    formdirectives.no_omit(IEditForm, 'campaign_pledge')

    representative_name = schema.TextLine(
        required=False,
        title=_(
            u"Name of your organisation's health and safety representative"),
    )
    directives.languageindependent('representative_name')
    formdirectives.omitted('representative_name')
    formdirectives.no_omit(IEditForm, 'representative_name')

    representative_email = schema.TextLine(
        required=False,
        title=_(
            u"Email address of your organisation's health and safety "
            "representative"),
        constraint=isEmail,
    )
    directives.languageindependent('representative_email')
    formdirectives.omitted('representative_email')
    formdirectives.no_omit(IEditForm, 'representative_email')

    representative_phone = schema.TextLine(
        required=False,
        title=_(
            u"Telephone number of your organisation's health and safety "
            "representative"),
    )
    directives.languageindependent('representative_phone')
    formdirectives.omitted('representative_phone')
    formdirectives.no_omit(IEditForm, 'representative_phone')

    mission_statement = schema.Text(
        title=_(u"Your mission statement"),
        description=_(u"Briefly outline the mission of your company"),
    )
    directives.languageindependent('mission_statement')
    formdirectives.omitted('mission_statement')
    formdirectives.no_omit(IEditForm, 'mission_statement')

    logo = NamedBlobImage(
        title=_(u"Company / Organisation logo"),
        description=_(
            u"Please add an image with the company / organisation logo. "
            u"Please use a format suited for web display if possible (JPEG, "
            u"PNG or GIF).")
    )
    directives.languageindependent('logo')
    formdirectives.omitted('logo')
    formdirectives.no_omit(IEditForm, 'logo')

    ceo_image = NamedBlobImage(
        title=_(u"Photo of your CEO, President, General Director or other"),
    )
    directives.languageindependent('ceo_image')
    formdirectives.omitted('ceo_image')
    formdirectives.no_omit(IEditForm, 'ceo_image')


class IOrganisationExtra(model.Schema):

    phase_1_intro = RichText(
        title=_("Introduction"),
        required=False,
    )
    formdirectives.omitted('phase_1_intro')
    formdirectives.no_omit(IAddForm, 'phase_1_intro')

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

    phase_2_intro = RichText(
        title=_("Introduction"),
        required=False,
    )
    formdirectives.omitted('phase_2_intro')
    formdirectives.no_omit(IEditForm, 'phase_2_intro')

    ceo_name = schema.TextLine(
        title=_(u"CEO"),
        description=_(
            u"Name / surname of your CEO, President, General Director or "
            "other"),
    )
    directives.languageindependent('ceo_name')
    formdirectives.omitted('ceo_name')
    formdirectives.no_omit(IEditForm, 'ceo_name')

    ceo_position = schema.TextLine(
        title=_(u"Position identifier"),
        description=_(
            u"Please indicate the actual position, such as President, General "
            "Director, CEO, Chairman, etc"),
        default=u"CEO",
    )
    directives.languageindependent('ceo_position')
    formdirectives.omitted('ceo_position')
    formdirectives.no_omit(IEditForm, 'ceo_position')

    description = schema.Text(
        title=_(
            u'His / her quote on the Healthy Workplaces Campaign on "Working '
            'together for risk prevention"'),
    )
    directives.languageindependent('description')
    formdirectives.omitted('description')
    formdirectives.no_omit(IEditForm, 'description')

    organisation_type = schema.Choice(
        title=_(u"Organisation type"),
        vocabulary=vocabularies.organisation_types,
    )
    directives.languageindependent('organisation_type')

    key_position = schema.TextLine(
        title=_(u"Position of the main contact person."),
    )
    directives.languageindependent('key_position')


class IOrganisation(IOrganisationBase, IOrganisationExtra):

    model.fieldset(
        'about_organisation',
        label=_(u'About your organisation'),
        fields=[
            'countries', 'additional_countries', 'title', 'organisation_type',
            'business_sector', 'social_dialogue', 'street', 'address_extra',
            'city', 'zip_code', 'country', 'email', 'phone', 'fax', 'key_name',
            'key_position', 'key_email', 'key_phone', 'url', 'campaign_url',
        ],
    )

    # About your involvement in the Campaign
    model.fieldset(
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

    model.fieldset(
        'additional_information',
        label=_(u"Additional information"),
        fields=[
            'mission_statement', 'ceo_name', 'ceo_position', 'description',
            'representative_name', 'representative_email',
            'representative_phone', 'logo', 'ceo_image', 'campaign_pledge']
    )


class AddForm(dexterity.AddForm):
    grok.name('osha.hwccontent.organisation')
    grok.context(IOrganisation)
    grok.require("osha.hwccontent.AddOrganisation")

    fields = field.Fields(IOrganisation).select(
        'phase_1_intro')

    def updateWidgets(self):
        super(AddForm, self).updateWidgets()
        self.widgets['phase_1_intro'].value = RichTextValue(
            INTRO_TEXT_PHASE_1, "text/html", "text/html")
        self.widgets['phase_1_intro'].mode = 'display'


class EditForm(dexterity.EditForm):
    grok.context(IOrganisation)
    grok.require("osha.hwccontent.AddOrganisation")

    def updateWidgets(self):
        # XXX: Here, determine if we are still in phase 2, i.e. if the user
        # still needs to fill the additional information fields
        # For the moment, we just check if one of the required fields from
        # phase 1 is still none
        is_phase_2 = self.context.mission_statement is None
        if is_phase_2:
            self.fields = field.Fields(IOrganisation).select('phase_2_intro')
        else:
            self.fields = field.Fields()
        super(EditForm, self).updateWidgets()
        if is_phase_2:
            self.widgets['phase_2_intro'].value = RichTextValue(
                INTRO_TEXT_PHASE_2, "text/html", "text/html")
            self.widgets['phase_2_intro'].mode = 'display'
