from Products.Five import BrowserView
from plone import api
from StringIO import StringIO
from osha.hwccontent.organisation import IOrganisation
from osha.hwccontent.focalpoint import IFocalPoint
from osha.hwccontent.mediapartner import IMediaPartner
from zope.schema import getFieldsInOrder
import csv


def fullname_from_userid(userid):
    user = api.user.get(userid)
    if user is None:
        return u""
    name = user.fullname or userid
    return name.encode('UTF8')


class PartnerReportView(BrowserView):
    '''@@activity-report lists all document activity since last report run.'''

    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')

        # Find all the organisation folders
        folders = catalog(portal_type='osha.hwccontent.organisationfolder')
        paths = [x.getPath() for x in folders]

        query = {'portal_type': ['osha.hwccontent.organisation',
                                 'osha.hwccontent.focalpoint',
                                 'osha.hwccontent.mediapartner',
                                 ],
                 'path': paths,
                 'Language': 'all',
                 'sort_on': 'modified',
                 }

        field_lists = {
            'osha.hwccontent.organisation': getFieldsInOrder(IOrganisation),
            'osha.hwccontent.focalpoint': getFieldsInOrder(IFocalPoint),
            'osha.hwccontent.mediapartner': getFieldsInOrder(IMediaPartner),
            }
        
        fieldnames = []
        for fields in field_lists.values():
            for fieldid, field in fields:
                if fieldid not in fieldnames:
                    fieldnames.append(fieldid)
                    
        results = []
        for partner in catalog(**query):
            ob = partner.getObject()
            p = {}
            for fieldid, field in field_lists[ob.portal_type]:
                v = field.get(ob)
                if isinstance(v, unicode):
                    v = v.encode('utf8')
                p[fieldid] = v

            results.append(p)

        # Dump to CSV
        csvfile = StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in sorted(results, key=lambda x: x['title']):
            writer.writerow(result)

        response = self.request.response
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=hwc2014-partner-report.csv",
        )
        response.setHeader(
            "Content-Type", 'text/comma-separated-values;charset=utf-8')

        return csvfile.getvalue()
