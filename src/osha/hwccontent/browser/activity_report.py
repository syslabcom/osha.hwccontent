from DateTime import DateTime
from Products.Five import BrowserView
from plone import api
from StringIO import StringIO
import csv

def fullname_from_userid(userid):
    user = api.user.get(userid)
    return user.fullname or userid
    
class ActivityReportView(BrowserView):
    '''@@activity-report lists all document activity since last report run.'''
    
    def __call__(self):
        catalog = api.portal.get_tool('portal_catalog')
        workflow = api.portal.get_tool('portal_workflow')
        types = api.portal.get_tool('portal_types')
        
        site_properties = api.portal.get_tool('portal_properties').site_properties
        if not site_properties.hasProperty('last_activity_report'):
            site_properties._setProperty('last_activity_report', '', 'string')

        # Find all the organisation folders
        folders = catalog(portal_type='osha.hwccontent.organisationfolder')
        paths = [x.getPath() for x in folders]

        query = {'portal_type': ['osha.hwccontent.organisation',
                                 'osha.hwccontent.focalpoint',
                                 'osha.hwccontent.mediapartner',
                                 'Event','Document',
                                 'Folder',
                                 'File',
                                 'News Item',
                                 ],
                 'path': paths,
                 }
        
        last_report = site_properties.getProperty('last_activity_report')
        
        if last_report:
            last_report_time = DateTime(last_report)
            query['modified'] = {'query': last_report_time, 'range': 'min'}
        else:
            last_report_time = DateTime(2000, 1, 1, 12, 00)

        results = catalog(**query)      

        # Figure out actions.
        events = []
        for result in results:
            # We have to load objects to check parents and workflow
            ob = result.getObject()

            # Get the portal type title:
            portal_type = types[ob.portal_type].title_or_id()
            
            # Find the partner:
            maybe_partner = ob
            while True:
                if maybe_partner.portal_type == 'osha.hwccontent.organisation':
                    partner = maybe_partner.title_or_id()
                    break
                maybe_partner = maybe_partner.aq_parent
                if not hasattr(maybe_partner, 'portal_type'):
                    # We are outside the site now.
                    partner = ''
                    break
                
            # URL
            url = ob.absolute_url()
            
            # Find transitions since last report:
            if hasattr(ob, 'workflow_history'):
                for wfname, changes in ob.workflow_history.items():
                    transitions = workflow.getWorkflowById(wfname).transitions
                    for change in changes:
                        if change['time'] < last_report_time:
                            continue
                        action = change['action']
                        if not action:
                            # Initial transition
                            continue
                        events.append({
                            'Partner': partner,
                            'Event': transitions[action].actbox_name + ' ' + portal_type,
                            'Date': change['time'].strftime('%Y-%m-%d %H:%M'),
                            'URL': url,
                            'Author': fullname_from_userid(change['actor']),
                        })
            
            if ob.created > last_report_time:
                action = 'New'
                user = ob.Creator()
            else:
                import pdb;pdb.set_trace()
                action = 'Modified'
                creators = ob.listCreators()
                if len(creators) > 1:
                    # More than one. Let's assume that the last author was not the creator:
                    creators.remove(doc.Creator())
                user = creators[-1]

            events.append({
                'Partner': partner,
                'Event': action + ' ' + portal_type,
                'Date': ob.modified().strftime('%Y-%m-%d %H:%M'),
                'URL': url,
                'Author': fullname_from_userid(user),
            })
        
        # Update the last report time
        site_properties._setPropValue('last_activity_report', DateTime().rfc822())
        
        # Dump to CSV
        csvfile = StringIO()
        writer = csv.DictWriter(csvfile, fieldnames=['Partner', 'Event', 'Date', 'URL', 'Author'])
        writer.writeheader()

        for event in sorted(events, key=lambda x: x['Partner']):
            writer.writerow(event)

        response = self.request.response
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=hwc2014-activity-report.csv",
        )
        response.setHeader(
            "Content-Type", 'text/comma-separated-values;charset=utf-8')
            
        return csvfile.getvalue()
    