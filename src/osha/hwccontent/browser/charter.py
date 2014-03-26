from Acquisition import aq_inner
from osha.hwccontent import _
from osha.hwccontent.interfaces import IFullWidth
from Products.CMFDefault.exceptions import EmailAddressInvalid
from Products.CMFDefault.utils import checkEmailAddress
from Products.CMFCore.utils import getToolByName
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
from plone.app.layout.navigation.root import getNavigationRootObject
from zope.annotation.interfaces import IAnnotations
from zope.i18n import translate
from zope.interface import implements

import csv
import json
import time

PRIVACY_POLICY_NAME = "privacy-policy-certificate-of-participation"

log = getLogger(__name__)

# consider translating the strings
email_template = _(u"charter_feedback_email_text", default=u"""<p>Thank you for actively supporting the Healthy Workplaces Campaign!</p>

<p>Please find a PDF version of the Campaign certificate attached to this email, which you may print.</p>

<p>For more information on the Healthy Workplaces Campaign, please
visit the website at http://www.healthy-workplaces.eu.</p>

<p>To keep up to date with the latest news, subscribe to EU-OSHA newsletter https://osha.europa.eu/en/news/oshmail/</p>
""")


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

    msg['Subject'] = "Healthy Workplaces Campaign Certificate"
    msg['From'] = sender
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    params = dict(charset='utf-8')
    part = MIMEBase('text', 'html', **params)
    part.set_payload(body)
    msg.attach(part)

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(pdf)
    Encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        'attachment; filename="campaign-certificate.pdf"',
    )
    msg.attach(part)

    mailhost._send(sender, to, msg.as_string())


class NationalPartnerForm(BrowserView):
    """ """
    implements(IFullWidth)

    def get_validation_messages(self):
        """ """
        data = self.get_translated_validation_messages()
        return json.dumps(data)

    def get_privacy_link(self):
        portal = api.portal.get()
        root = getNavigationRootObject(self.context, portal)
        document = root.restrictedTraverse(PRIVACY_POLICY_NAME, None)
        if document:
            return document.absolute_url()
        else:
            log.error('Privacy policy document "{0}" not found under {1}'.format(
                PRIVACY_POLICY_NAME, root.absolute_url()))
            return ""

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
            'privacy': translate(_(u'Privacy')),
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

    def __call__(self, form=None, errors={}):
        self.form = form
        self.errors = errors
        request = self.context.REQUEST
        if 'form.submitted' not in request.form:
            return super(
                NationalPartnerForm, self).__call__(self.context, self.request)

        language = self.context.portal_languages.getPreferredLanguage()
        messages = IStatusMessage(request)
        portal = getToolByName(self, 'portal_url').getPortalObject()
        from_address = portal.getProperty('email_from_address', '')

        url = "/%s/get-involved/get-your-certificate/feedback" % language

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
        privacy = request.get('privacy', False)

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
            "telephone": telephone,
            "privacy": privacy,
        }

        error_messages = self.get_translated_validation_messages()["messages"]
        has_errors = False
        errors = {}
        for required_field in required_fields.keys():
            if required_field == "email":
                try:
                    checkEmailAddress(required_fields.get(required_field, ""))
                except EmailAddressInvalid:
                    has_errors = True
                    messages.add(
                        error_messages[required_field]["email"],
                        type=u"error")
                    errors[required_field] = error_messages[required_field]["email"]
            elif required_field == 'privacy':
                if not required_fields.get(required_field, False):
                    has_errors = True
                    messages.add(
                        error_messages[required_field]["required"],
                        type=u"error")
                    errors[required_field] = error_messages[required_field]["required"]
            elif required_fields[required_field].strip() == "":
                has_errors = True
                messages.add(
                    error_messages[required_field]["required"],
                    type=u"error")
                errors[required_field] = error_messages[required_field]["required"]
        if has_errors:
            if 'form.submitted' in request.form:
                del request.form['form.submitted']
            form_path = (
                "%s/@@get-campaign-certificate"
                % "/".join(self.context.getPhysicalPath()))
            return self.context.restrictedTraverse(
                form_path)(form=request.form, errors=errors)

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
                sender="Healthy Workplaces <%s>" % from_address,
                body=translate(email_template, target_language=language,).encode('utf-8'),
                language=language,
            )
        #XXX Too many things could possibly go wrong. So we catch all.
        except Exception, e:
            exception = self.context.plone_utils.exceptionString()
            logit("Exception: " + exception)
            raise
            return request.RESPONSE.redirect(
                url + '?portal_status_message=' + str(e))

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
        portal = api.portal.get()
        participant_details = IAnnotations(portal.participants)
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
        writer.writerow(dict((fn, fn) for fn in fieldnames))
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
