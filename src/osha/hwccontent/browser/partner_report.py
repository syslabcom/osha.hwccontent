from Products.Five import BrowserView
from plone import api
from StringIO import StringIO
from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.mediapartner import IMediaPartner
from plone.app.textfield.value import RichTextValue
from zope.schema import getFieldsInOrder
import xlrd
import xlwt


def fullname_from_userid(userid):
    user = api.user.get(userid)
    if user is None:
        return u""
    name = user.fullname or userid
    return name.encode('UTF8')


class OFMReportViewBase(BrowserView):

    portal_types = []
    report_name = 'base'

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        workflow = api.portal.get_tool('portal_workflow')

        # Find all the organisation folders
        folders = catalog(portal_type='osha.hwccontent.organisationfolder')
        paths = [x.getPath() for x in folders]

        query = {'portal_type': self.portal_type,
                 'path': paths,
                 'Language': 'all',
                 'sort_on': 'modified',
                 }

        field_lists = {
            'osha.hwccontent.organisation': getFieldsInOrder(IOrganisation),
            'osha.hwccontent.mediapartner': getFieldsInOrder(IMediaPartner),
        }

        skip_fields = [
            'phase_1_intro', 'phase_2_intro', 'privacy_policy_text', 'logo',
            'ceo_image', 'Description', 'privacy_policy',
        ]
        fieldnames = []
        fieldtitles = []

        for fieldid, field in field_lists[self.portal_type]:
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
        top_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
        normal_xf = xlwt.easyxf('align: wrap off, vert top, horiz left')
        for col, fn in enumerate(fieldtitles):
            ws.write(0, col, fn, top_xf)

        row = 1
        for data in sorted(results, key=lambda x: x['title']):
            for col, fn in enumerate(fieldnames):
                ws.write(row, col, data.get(fn, ''), normal_xf)
            row += 1

        buffer = StringIO()
        wb.save(buffer)
        read_book = xlrd.open_workbook(file_contents=buffer.getvalue(), formatting_info=True)
        read_sheet = read_book.sheet_by_index(0)
        for i in range(read_sheet.ncols):
            width = 0
            for j in range(read_sheet.nrows):
                size = min(len(read_sheet.cell(j, i).value), 50)
                width = max(width, size)
            ws.col(i).width = width * 200

        ws.set_remove_splits(True)  # if user does unfreeze, don't leave a split there
        ws.set_horz_split_pos(1)
        ws.set_vert_split_pos(0)
        ws.set_panes_frozen(1)

        xlsfile = StringIO()
        wb.save(xlsfile)
        result = xlsfile.getvalue()
        buffer.close()
        xlsfile.close()

        response = self.request.response
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=hwc2014-%s-report.xls" % self.report_name,
        )
        response.setHeader(
            "Content-Type", 'application/vnd.ms-excel')

        return result


class MediapartnerReportView(OFMReportViewBase):

    portal_type = 'osha.hwccontent.mediapartner'
    report_name = 'mediapartners'


class OrganisationReportView(OFMReportViewBase):

    portal_type = 'osha.hwccontent.organisation'
    report_name = 'official-campaign-partners'
