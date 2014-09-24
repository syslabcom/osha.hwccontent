# _+- coding: utf-8 -*-

from collective.z3cform.datagridfield import DictRow
from five import grok
from plone.app.contenttypes.interfaces import IFile
from plone.app.textfield import RichText
from plone.directives import form
from plone.supermodel import model
from zope import schema
from Products.CMFCore.utils import getToolByName
from osha.hwccontent import vocabularies
from osha.hwccontent.behaviors.moreabout import CustomTableWidgetFactory

from zope.component.hooks import getSite
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class ITableRowSchema(form.Schema):
    country = schema.Choice(
        title=u"Country",
        vocabulary=vocabularies.countries_no_pan_euro,
    )

    language = schema.Choice(
        title=u"Language",
        vocabulary='osha.languages',
    )

    attachment = schema.Choice(
        title=u"File (download)",
        source="osha.eguides",
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

    eguides = schema.List(
        title=u"Related sites",
        required=False,
        value_type=DictRow(
            title=u"tablerow",
            required=False,
            schema=ITableRowSchema,),
    )
    form.widget(eguides=CustomTableWidgetFactory)


@implementer(IVocabularyFactory)
class LocalFilesVocabulary(object):
    """
    This is a (deliberate) hack! Since context is not preserved in a datagridfield,
    we simply search for items of our own content type, and take the first hit
    to look for the files contained in it.
    It is up to the site maintainer to make sure there is only ever one
    eguide-storage.
    See https://github.com/collective/collective.z3cform.datagridfield/issues/31
    """

    def __call__(self, context):
        files = []
        site = getSite()
        catalog = getToolByName(site, 'portal_catalog')
        res = catalog(portal_type="osha.hwccontent.eguide_storage")
        if len(res):
            storage = res[0].getObject()
            files = [
                x for x in storage.objectItems() if IFile.providedBy(x[1])]

        return SimpleVocabulary(
            [SimpleTerm(value=item[0], title=item[1].Title) for item in files])

grok.global_utility(LocalFilesVocabulary, name='osha.eguides')
