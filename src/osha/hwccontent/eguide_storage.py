# _+- coding: utf-8 -*-

from collective.z3cform.datagridfield import DictRow
from plone.directives import form
from plone.namedfile.field import NamedBlobFile
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

    attachment = NamedBlobFile(
        title=u"File (download)",
        required=False,
    )

    url = schema.URI(
        title=u"Link (online)",
        required=False,
    )


class IEguideStorage(model.Schema):

    eguides = schema.List(
        title=u"Related sites",
        required=False,
        value_type=DictRow(
            title=u"tablerow",
            required=False,
            schema=ITableRowSchema,),
    )
    form.widget(eguides=CustomTableWidgetFactory)
