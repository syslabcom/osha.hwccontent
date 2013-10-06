# -*- coding: utf-8 -*-
from collective.z3cform.datagridfield import DataGridField
from collective.z3cform.datagridfield import DictRow
from osha.hwccontent import _
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.directives import form
from plone.formwidget.contenttree import (
    MultiContentTreeFieldWidget,
    ObjPathSourceBinder,
)
from plone.multilingualbehavior import directives
from plone.supermodel import model
from z3c.form import interfaces
from z3c.form.widget import FieldWidget
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import component
from zope import interface
from zope import schema
from zope.component import adapts
from zope.schema.interfaces import IField


class ICustomTableWidget(interface.Interface):
    """Subclass the widget, required for template customization"""


@interface.implementer(ICustomTableWidget)
class CustomTableWidget(DataGridField):
    """This grid should be applied to an schema.List item which has
       schema.Object and an interface"""

    allow_insert = True
    allow_delete = True
    allow_reorder = True
    auto_append = True


@component.adapter(IField, interfaces.IFormLayer)
@interface.implementer(interfaces.IFieldWidget)
def CustomTableWidgetFactory(field, request):
    """IFieldWidget factory for DataGridField."""
    return FieldWidget(field, CustomTableWidget(request))


class ITableRowSchema(form.Schema):
    label = schema.TextLine(
        title=_(u"Title"),
        required=False,
    )
    url = schema.URI(
        title=_(u"URL"),
        required=False,
    )


@interface.provider(IFormFieldProvider)
class IRelatedSites(model.Schema):
    """Marker / Form interface for additional links """

    model.fieldset('settings', label=_(u"Settings"),
                   fields=['related_sites_links'])

    related_sites_links = schema.List(
        title=_(u"Related sites"),
        required=False,
        value_type=DictRow(
            title=_(u"tablerow"),
            required=False,
            schema=ITableRowSchema,),
    )
    form.widget(related_sites_links=CustomTableWidgetFactory)


@interface.implementer(IRelatedSites)
class RelatedSites(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


@interface.provider(IFormFieldProvider)
class ISeeAlso(model.Schema):
    """Marker / Form interface for internal references"""

    model.fieldset('settings', label=_(u"Settings"),
                   fields=['see_also'])

    see_also = RelationList(
        title=_(u"See also"),
        description=_(u"Pick existing items"),
        required=False,
        value_type=RelationChoice(
            title=_(u"Select an existing item"),
            required=False,
            source=ObjPathSourceBinder(),
        ),
    )

    form.widget(see_also=MultiContentTreeFieldWidget)
    directives.languageindependent('see_also')


@interface.implementer(ISeeAlso)
class SeeAlso(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context


@interface.provider(IFormFieldProvider)
class ISectionImage(form.Schema):
    """Marker / Form interface for adding section image(s)"""

    model.fieldset('settings', label=_(u"Settings"),
                   fields=['section_image'])

    section_image = RelationList(
        title=_(u"Section images"),
        description=_(u"Pick one or more existing images"),
        required=False,
        value_type=RelationChoice(
            title=_(u"Browse for images in the site"),
            required=False,
            source=ObjPathSourceBinder(portal_type='Image'),
        ),
    )

    form.widget(section_image=MultiContentTreeFieldWidget)
    directives.languageindependent('section_image')


@interface.implementer(ISectionImage)
class SectionImage(object):
    adapts(IDexterityContent)

    def __init__(self, context):
        self.context = context
