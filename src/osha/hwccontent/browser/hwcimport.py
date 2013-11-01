# -*- coding: utf-8 -*-
        
from Products.CMFCore.interfaces import ISiteRoot
from five import grok
from osha.hwccontent.focalpoint import IFocalPoint
from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent import events
from plone.api import content
from plone.app.textfield.interfaces import IRichText
from plone.app.textfield.value import RichTextValue
from plone.directives import form
from plone.namedfile.file import NamedBlobImage
from plone.namedfile.interfaces import INamedImageField
from z3c.form import button
from zope import schema
from zope.schema import getFieldsInOrder
import base64
import json
import logging
logger = logging.getLogger('HWC Partner Import')

class IHWCImportForm(form.Schema):

    json = schema.Bytes(
            title=u"JSON file",
        )

class HWCImportForm(form.SchemaForm):
    """ Define Form handling

    This form can be accessed as http://yoursite/@@my-form

    """
    grok.name('hwcimport')
    grok.require('cmf.ManagePortal')
    grok.context(ISiteRoot)

    schema = IHWCImportForm
    ignoreContext = True

    label = u"HWC Import form"
    description = u"Import organisations and focal points from the old campaign site."

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
                
        events._send_emails = False
        try:
            
            en_folder = self.context.restrictedTraverse('en')
            if 'organisations' in en_folder:
                org_folder = en_folder.restrictedTraverse('organisations')
            else:
                org_folder = content.create(en_folder,
                                            type='osha.hwccontent.organisationfolder',
                                            title='Organisations')
            if 'focalpoints' in en_folder:
                fop_folder = en_folder.restrictedTraverse('focalpoints')
            else:
                fop_folder = content.create(en_folder,
                                            type='osha.hwccontent.organisationfolder',
                                            title='Focalpoints')
        
            type_mapping = {
                u'Organisation': {
                    'type': 'osha.hwccontent.organisation',
                    'schema': dict(getFieldsInOrder(IOrganisation)),
                    'folder': org_folder,
                    'wf_actions': ('approve_phase_1',),
                },
                    
                u'Focalpoint': {
                    'type': 'osha.hwccontent.focalpoint',
                    'schema': dict(getFieldsInOrder(IFocalPoint)),
                    'folder': fop_folder,
                    'wf_actions': ('publish',),
                }
            }
    
            count = 0
            for data in json.loads(data['json']):
                
                # Only keep the data that's in the main schema:
                type_info = type_mapping[data['_type']]
                schema = type_info['schema']
                fields = {}
                
                if data['title'].startswith('MC-'):
                    continue
                
                for name, field in schema.items():
                    if name in data:
                        value = data[name]
                        if value and INamedImageField.providedBy(field):
                            content_type = data.get('_%s_content_type' % name, '')
                            filename = data.get('_%s_filename' % name , None)
                            value = NamedBlobImage(base64.b64decode(value), str(content_type), filename)
                        elif value and IRichText.providedBy(field):
                            content_type = data.get('_%s_content_type', None)
                            value = RichTextValue(value, mimeType=content_type)
    
                        fields[name] = value
    
                new_obj = content.create(container=type_info['folder'],
                                         type= type_info['type'], 
                                         id=data['id'],
                                         **fields)
                for transition in type_info['wf_actions']:
                    try:
                        content.transition(new_obj, transition)
                    except Exception:
                        logger.exception('Could not execute %s transition for %s' % (transition, '/'.join(new_obj.getPhysicalPath())))
                        
                logger.info('Imported %s' % new_obj.getId())
                count += 1
    
            # Set status on this form page
            self.status = "%s partners imported" % count
        except Exception:
            # Enable emails again:
            events._send_emails = True
            raise

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """

        