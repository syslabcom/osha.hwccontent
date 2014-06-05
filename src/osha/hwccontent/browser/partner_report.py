from Products.Five import BrowserView
from plone import api
from StringIO import StringIO
from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.focalpoint import IFocalPoint
from osha.hwccontent.mediapartner import IMediaPartner
from plone.app.textfield.value import RichTextValue
from zope.schema import getFieldsInOrder
import xlwt


def fullname_from_userid(userid):
    user = api.user.get(userid)
    if user is None:
        return u""
    name = user.fullname or userid
    return name.encode('UTF8')


class OFMReportViewBase(BrowserView):
    
    portal_types = []
    report_name ='base'

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        workflow = api.portal.get_tool('portal_workflow')

        # Find all the organisation folders
        folders = catalog(portal_type='osha.hwccontent.organisationfolder')
        paths = [x.getPath() for x in folders]

        query = {'portal_type': self.portal_types,
                 'path': paths,
                 'Language': 'all',
                 'sort_on': 'modified',
                 }

        field_lists = {
            'osha.hwccontent.organisation': getFieldsInOrder(IOrganisation),
            'osha.hwccontent.focalpoint': getFieldsInOrder(IFocalPoint),
            'osha.hwccontent.mediapartner': getFieldsInOrder(IMediaPartner),
            }
        
        skip_fields = {'phase_1_intro', 'phase_2_intro', 'privacy_policy_text', 'logo', 'ceo_image'}
        fieldnames = []
        fieldtitles = []
        
        for fields in field_lists.values():
            for fieldid, field in fields:
                if fieldid in skip_fields:
                    continue
                if fieldid not in fieldnames:
                    fieldnames.append(fieldid)
                    fieldtitles.append(field.title.encode('utf8'))
        
        fieldnames.append('workflow_status')
        fieldtitles.append('Workflow Status')
                    
        results = []
        for partner in catalog(**query):
            ob = partner.getObject()
            p = {}
            for fieldid, field in field_lists[ob.portal_type]:
                if fieldid in skip_fields:
                    continue

                v = field.get(ob)
                
                if fieldid == 'social_media':
                    v = ', '.join('%s: %s' % (x['label'], x['url']) for x in v)
                elif v is None:
                    v = ''
                elif isinstance(v, (list, tuple, set)):
                    v = ', '.join(v)
                elif isinstance(v, RichTextValue):
                    v = v.output
                elif isinstance(v, bool):
                    v = str(v)

                if isinstance(v, unicode):
                    v = v.encode('utf8')

                p[fieldid] = v

            state = api.content.get_state(ob)
            p['workflow_status'] = workflow.getTitleForStateOnType(state, ob.portal_type)
            results.append(p)

        # Dump to XLS                
        wb = xlwt.Workbook(encoding='utf8')
        ws = wb.add_sheet('Participants')
        for col, fn in enumerate(fieldtitles):
            ws.write(0, col, fn)

        row = 1
        for data in sorted(results, key=lambda x: x['title']):
            for col, fn in enumerate(fieldnames):
                ws.write(row, col, data.get(fn, ''))
            row += 1

        xlsfile = StringIO()        
        wb.save(xlsfile)
        result = xlsfile.getvalue()
        xlsfile.close()
        
        response = self.request.response
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=hwc2014-%s-report.xls" % self.report_name,
        )
        response.setHeader(
            "Content-Type", 'application/vnd.ms-excel')

        return result


class PartnerReportView(OFMReportViewBase):
    
    portal_types =  ['osha.hwccontent.mediapartner',
                     ]
    report_name ='mediapartner'
    

class OrgFocReportView(OFMReportViewBase):

    portal_types =  ['osha.hwccontent.organisation',
                     'osha.hwccontent.focalpoint',
                     ]
    report_name ='organisation-focalpoint'
    