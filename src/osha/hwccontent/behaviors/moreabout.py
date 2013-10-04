# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow
from osha.hwccontent import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from plone.supermodel import model
from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from zope.interface import alsoProvides, implements
from zope import component
from zope import interface
from zope import schema
from zope.component import adapts
from zope.schema.interfaces import IField


class IFixedTableWidget(interface.Interface):
    """Subclass the widget, required for template customization"""


class FixedTableWidget(DataGridField):
    """This grid should be applied to an schema.List item which has
       schema.Object and an interface"""

    interface.implements(IFixedTableWidget)

    allow_insert = True
    allow_delete = True
    allow_reorder = True
    auto_append = True


@component.adapter(IField, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def FixedTableWidgetFactory(field, request):
    """IFieldWidget factory for DataGridField."""
    return FieldWidget(field, FixedTableWidget(request))


class ITableRowSchema(form.Schema):
    label = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )
    url = schema.URI(
        title=_(u"URL"),
        required=False,
    )


class IRelatedSites(model.Schema):
    """Marker / Form interface for additional links """

    see_also_links = schema.List(
        title=_(u"See also"),
        required=False,
        value_type=DictRow(
            title=_(u"tablerow"),
            required=False,
            schema=ITableRowSchema,),
    )
    form.widget(see_also_links=FixedTableWidgetFactory)

alsoProvides(IRelatedSites, IFormFieldProvider)


class RelatedSites(object):
    implements(IRelatedSites)
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
