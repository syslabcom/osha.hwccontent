# _+- coding: utf-8 -*-

from collective.z3cform.datagridfield import DictRow
from plone.app.textfield import RichText
from plone.directives import form
from plone.supermodel import model
from zope import schema
from osha.hwccontent import vocabularies
from osha.hwccontent.behaviors.moreabout import CustomTableWidgetFactory


class ITableRowSchema(form.Schema):
    country = schema.Choice(
        title=u"Country",
        vocabulary=vocabularies.countries_no_pan_euro,
    )

    language = schema.Choice(
        title=u"Language",
        vocabulary='osha.languages',
    )

    download_url = schema.URI(
        title=u"Download (file)",
        required=False,
    )

    url = schema.URI(
        title=u"Link (online)",
        required=False,
    )


class IEguideStorage(model.Schema):

    title = schema.TextLine(
        title=u"Title",
    )

    text = RichText(
        title=u"Text",
        required=False,
    )
    generic_eguide_text = RichText(
        title=u"Text about the e-guide",
        description=u"This text will appear next to the download box of the"
        u"generic e-guide.",
        required=False,
    )
    instructions_text = RichText(
        title=u"Instructions",
        description=u"These will be displayed at the bottom of the page.",
        required=False,
    )
    film_id = schema.TextLine(
        title=u"YouTube film id",
        description=
        u"Paste here the ID of a film on YouTube to show. "
        u"Example: For a movie like http://www.youtube.com/watch?v=iBy4WaR14Bo"
        u" the ID is iBy4WaR14Bo",
        required=False,
    )

    generic_guide_url = schema.URI(
        title=u"Link (online)",
        required=False,
    )

    eguides = schema.List(
        title=u"Related sites",
        required=False,
        value_type=DictRow(
            title=u"tablerow",
            required=False,
            schema=ITableRowSchema,),
    )
    form.widget(eguides=CustomTableWidgetFactory)
