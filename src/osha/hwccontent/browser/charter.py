from Acquisition import aq_inner
from Products.Archetypes import PloneMessageFactory as _
from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.CMFDefault.utils import checkEmailAddress
from Products.Five.browser import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from StringIO import StringIO
from email import Encoders
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.Utils import formatdate
from generate_pdf import generatePDF
from logging import getLogger
from plone import api
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate

import csv
import json
import time

log = getLogger('osha.hw2014.browser.charter')

# consider translating the strings
email_template = """<p>Thank you for signing the European Week Charter.</p>

<p>Please find a PDF version of the charter attached to this email,
which you may print.</p>

<p>For more information on the Healthy Workplaces Campaign, please
consult the website at http://www.healthy-workplaces.eu.</p>


"""


def logit(*kwargs):
    " log something from the web "
    try:
        mesg = ''
        for kwarg in kwargs:
            mesg += str(kwarg) + ' '
        print mesg
    except:
        print [kwargs]


def send_charter_email(context, pdf, to, sender, body, language):
    """ sending the charter by mail """
    mailhost = context.MailHost
    msg = MIMEMultipart()

    msg['Subject'] = "The Healthy Workplaces 2012 Campaign Charter"
    msg['From'] = sender
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    part = MIMEBase('text', 'html')
    part.set_payload(body)
    msg.attach(part)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf)
    Encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        'attachment; filename="hw2012-campaign-charter.pdf"',
    )
    msg.attach(part)

    mailhost._send(sender, to, msg.as_string())


class NationalPartnerForm(BrowserView):
    """ """
    def __call__(self, form=None):
        self.form = form
        return super(
            NationalPartnerForm, self).__call__(self.context, self.request)

    def get_validation_messages(self):
        """ """
        data = self.get_translated_validation_messages()
        return json.dumps(data)

    def get_translated_validation_messages(self):
        context = aq_inner(self.context)
        request = context.REQUEST
        fieldnames = {
            'organisation': translate(_('Company/Organisation')),
            'address': translate(_('Address')),
            'postal_code': translate(_('Postal Code')),
            'city': translate(_('City')),
            'country': translate(_('Country')),
            'firstname': translate(_('Firstname')),
            'lastname': translate(_('Lastname')),
            'sector': translate(_('Sector')),
            'email': translate(_('Email')),
            'telephone': translate(_('Telephone')),
        }
        messages = {}

        for field_id in fieldnames:
            fieldname = fieldnames[field_id]
            err_msgs = {
                'required': translate(
                    _(u'error_required',
                      default=u'${name} is required, please correct.',
                      mapping={'name': fieldname}),
                    context=request,
                ),

                'email': translate(
                    _(u"You entered an invalid email address."),
                    context=request,
                ),
            }

            messages[field_id] = err_msgs

        return {'messages': messages}


class CharterView(NationalPartnerForm):
    """ """

    def store_participant_details(self, details):
        """Store the details of the participant in a dict, using
        annotations (OOBTree) to avoid conflicts"""
        portal = api.portal.get()
        participants = portal.get("participants")
        if not participants:
            participants = api.content.create(
                container=portal, type="Document", id="participants")

        storage = IAnnotations(participants)
        key = time.time()
        storage[key] = details

    def __call__(self):

        request = self.context.REQUEST
        language = self.context.portal_languages.getPreferredLanguage()
        messages = IStatusMessage(request)

        url = "/%s/get-involved/become-a-national-partner/feedback" % language

        organisation = request.get('organisation', '')
        address = request.get('address', '')
        postal_code = request.get('postal_code', '')
        city = request.get('city', '')
        country = request.get('country', '')
        firstname = request.get('firstname', '')
        lastname = request.get('lastname', '')
        sector = request.get('sector', '')
        email = request.get('email', '')
        telephone = request.get('telephone', '')
        checkboxlist = request.get('checkboxlist', [])
        other = request.get('other_activities_text', '')

        required_fields = {
            "organisation": organisation,
            "address": address,
            "postal_code": postal_code,
            "city": city,
            "country": country,
            "firstname": firstname,
            "lastname": lastname,
            "sector": sector,
            "email": email,
            "telephone": telephone
        }

        error_messages = self.get_translated_validation_messages()["messages"]
        has_errors = False
        for required_field in required_fields.keys():
            if (required_field == "email"):
                try:
                    checkEmailAddress(required_fields.get(required_field, ""))
                except EmailAddressInvalid:
                    has_errors = True
                    messages.add(
                        error_messages[required_field]["email"],
                        type=u"error")
            elif required_fields[required_field].strip() == "":
                has_errors = True
                messages.add(
                    error_messages[required_field]["required"],
                    type=u"error")
        if has_errors:
            form_path = (
                "%s/@@national-campaign-partner-application-form-2012"
                % "/".join(self.context.getPhysicalPath()))
            return self.context.restrictedTraverse(
                form_path)(form=request.form)

        checkboxes = {}
        for c in checkboxlist:
            args = c.split('_', 1)
            if args[1] == 'other':
                args[1] = other
            checkboxes[int(args[0])] = args[1]

        checkbox_keys = [
            'seminars',
            'competitions',
            'audiovisual',
            'advertising',
            'partnerships',
            'good_neighbour',
            'hazard_spotting',
            'inspections',
            'initiatives',
        ]
        checkbox_options = {}
        for i, key in enumerate(checkbox_keys):
            checkbox_options[key] = checkboxes.get(i, '')

        participant_details = {
            'organisation': organisation,
            'address': address,
            'postal_code': postal_code,
            'city': city,
            'country': country,
            'firstname': firstname,
            'lastname': lastname,
            'sector': sector,
            'email': email,
            'telephone': telephone,
            'other': other,
        }
        participant_details.update(checkbox_options)
        self.store_participant_details(participant_details)

        from_address = 'information@osha.europa.eu'

        try:
            logit(" ... calling generatePDF, language: %s" % language)
            logit(" ... calling generatePDF")
            pdf = generatePDF(
                self.context,
                company=organisation,
                language=language,
                firstname=firstname,
                lastname=lastname,
                checkboxes=checkboxes,
                usePDFTK=0
            )

            logit(" ... generatePDF called!")
            send_charter_email(
                self.context,
                pdf=pdf,
                to=email,
                sender=from_address,
                body=email_template,
                language=language,
            )
        #XXX Too many things could possibly go wrong. So we catch all.
        except Exception, e:
            exception = self.context.plone_utils.exceptionString()
            logit("Exception: " + exception)
            raise
            return request.RESPONSE.redirect(
                url+'?portal_status_message='+str(e))

        request.RESPONSE.redirect(url)


class ParticipantsCSV(BrowserView):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        response = self.request.RESPONSE
        self.set_response_headers(response)
        return self.get_participants_as_csv()

    def get_participants_as_csv(self):
        buffer = StringIO()
        participant_details = IAnnotations(
            api.content.get(path="/participants"))
        fieldnames = [
            'organisation',
            'address',
            'postal_code',
            'city',
            'country',
            'firstname',
            'lastname',
            'sector',
            'email',
            'telephone',
            'seminars',
            'competitions',
            'audiovisual',
            'advertising',
            'partnerships',
            'good_neighbour',
            'hazard_spotting',
            'inspections',
            'initiatives',
            'other',
        ]
        writer = csv.DictWriter(
            buffer,
            fieldnames=fieldnames,
            delimiter=',',
            quotechar='|',
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writerow(dict((fn,fn) for fn in fieldnames))
        for key in participant_details:
            writer.writerow(participant_details[key])
        csv_data = buffer.getvalue()
        buffer.close()

        return csv_data

    def set_response_headers(self, response):
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=hwc2014-participants.csv",
        )
        response.setHeader(
            "Content-Type", 'text/comma-separated-values;charset=utf-8')
