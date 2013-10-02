# _+- coding: utf-8 -*-

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
from osha.hwccontent.organisation import IOrganisationBase


class IFocalPoint(IOrganisationBase):
    pass

