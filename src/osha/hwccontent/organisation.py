from Products.CMFCore.utils import getToolByName
from five import grok
from osha.hwccontent import _, vocabularies
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from plone.supermodel import model
from zope import schema

class IOrganisation(model.Schema):
    
    street = schema.TextLine(
        title = _(u"Street"),
    )
    
    address_extra = schema.TextLine(
        required=False,
        title = _(u"Address extra"),
    )
    
    city = schema.TextLine(
        title = _(u"City"),
    )
    
    zip_code = schema.TextLine(
        title = _(u"Zip code"),
    )

    country = schema.Choice(
        title = _(u"Country"),
        vocabulary = vocabularies.countries,
    )
    
    email = schema.TextLine(
        title = _(u"E-Mail"),
    )

    phone = schema.TextLine(
        title = _(u"Telephone number"),
    )
     
    fax = schema.TextLine(
        required=False,
        title = _(u"Fax number"),
    )

    url = schema.TextLine(
        title = _(u"Website"),
    )

    campaign_url = schema.TextLine(
        title = _(u"Dedicated Campaign Website"),
    )

    logo = NamedBlobImage(
        title = _(u"Company/Organisation logo"),
    )

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

    ceo_name = schema.TextLine(
        description = _(u"Name / surname of your CEO, President, General Director or other"),
        title = _(u"CEO"),
    )
    
    ceo_position = schema.TextLine(
        description = _(u"Please indicate the actual position, such as President, General Director, CEO, Chairman, etc"),
        title = _(u"Position identifier"),
    )
    
    key_name = schema.TextLine(
        description = _(u"Name/Surname of main contact person for the Campaign"),
        title = _(u"Contact person"),
    )

    key_position = schema.TextLine(
        title = _(u"Position of the main contact person."),
    )

    key_email = schema.TextLine(
        title = _(u"Email address of main contact person."),
    )

    key_phone = schema.TextLine(
        title = _(u"Telephone number of main contact person."),
    )

    representative_name = schema.TextLine(
        required=False,
        title = _(u"Name of your organisation\'s health and safety representative"),
    )

    representative_email = schema.TextLine(
        required=False,
        title = _(u"Email address of your organisation\'s health and safety representative"),
    )

    representative_phone = schema.TextLine(
        required=False,
        title = _(u"Telephone number of your organisation's health and safety representative"),
    )


class View(grok.View):
    grok.context(IOrganisation)
    grok.require('zope2.View')

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')
        
    def get_events(self):
        return self.portal_catalog(portal_type='Event', path=self.context.getPhysicalPath())
    
    def get_news(self):
        return self.portal_catalog(portal_type='News Item', path=self.context.getPhysicalPath())
    
    def get_news_folder_url(self):
        return self.context.restrictedTraverse('news').absolute_url()
    
    def get_events_folder_url(self):
        return self.context.restrictedTraverse('events').absolute_url()    