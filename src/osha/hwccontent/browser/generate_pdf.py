import os, tempfile
from StringIO import StringIO
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.colors import red, black, blue, green, HexColor
from reportlab.lib.enums import TA_CENTER
import reportlab.rl_config
from zope.i18n import translate
import xml.sax.saxutils as saxutils

reportlab.rl_config.warnOnMissingFontGlyphs = 0
HW2012BLUE = HexColor('#0a428f')

def generatePDF(self,

        company="European Agency for Safety and Health at Work",
        language='en',
        firstname='',
        lastname='',
        checkboxes={},
        usePDFTK=0):

    language = language.lower()

    if language not in [
                'bg', 'cs', 'da', 'de',
                'el', 'en', 'es', 'et',
                'fi', 'fr', 'hu', 'it',
                'lt', 'lv', 'mt', 'nl',
                'pl', 'ro', 'pt', 'sk', 'no', 'is',
                'sl', 'sv']:
        language = "en"

    ptt_domain = 'osha_ew'
    year = "2010"

    # create a canvas and set metadata
    acknowledge = StringIO()
    my_canvas = canvas.Canvas(acknowledge, pagesize=landscape(A4))
    my_canvas.setTitle('Charter of the Healthy Workplaces campaign')
    my_canvas.setAuthor('European Agency for Safety and Health at Work')
    my_canvas.setSubject('Charter of the Healthy Workplaces campaign')

    # register the font for writing company, name and actions
    pwd = os.path.dirname(__file__)
    resources_dir = os.path.realpath(os.path.join(pwd, "../resources"))
    font_dir = os.path.realpath(os.path.join(resources_dir, "fonts"))
    arial = font_dir + '/arial.ttf'
    pdfmetrics.registerFont( TTFont('Arial', arial) )
    arial_bold =  font_dir + '/arialbd.ttf'
    pdfmetrics.registerFont( TTFont('ArialBold', arial_bold) )
    arial_italic =  font_dir + '/ariali.ttf'
    pdfmetrics.registerFont( TTFont('ArialItalic', arial_italic) )
    arial_bi =  font_dir + '/arialbi.ttf'
    pdfmetrics.registerFont( TTFont('ArialBoldItalic', arial_bi) )
    arial_nb =  font_dir + '/arialnb.ttf'
    pdfmetrics.registerFont( TTFont('ArialNarrowBold', arial_nb) )
     # get the frontimage and write it to the canvas
    charterfilename = "charter_hw2012.jpg"
#     frontfile = getattr(self, charterfilename, None)
#     # Fallback to English
# #    if not frontfile:
# #        frontfile = getattr(self.charter_img, charterfilename % 'en')
#     frontdata = str(frontfile._data)
#     frontfile =StringIO(frontdata)
    frontimage = ImageReader(os.path.join(resources_dir, charterfilename))
    # my_canvas.drawImage(frontimage, 0 , 0, 87.5*cm, 123.8*cm)
    my_canvas.drawImage(frontimage, 0 , 0, 29.7*cm, 21*cm)

    msg_id = 'campaign_name_'+year
    u_campaign_name = translate(
                                domain=ptt_domain,
                                msgid=msg_id,
                                target_language=language,
                                context=self
                                )
    x = 14.85 * cm
    y = 19 * cm
    my_canvas.setFillColor(HW2012BLUE)
    my_canvas.setFont('ArialBold', 20)
    my_canvas.drawCentredString(x, y, u_campaign_name.upper())
    print " +- set Heading"
    mapping = {'campaign_slogan':u_campaign_name, 'year':year}

    msg_id = 'campaign_slogan_'+year
    u_campaign_slogan = translate(
                                domain=ptt_domain,
                                msgid=msg_id,
                                target_language=language,
                                context=self
                                )
    x = 14.85 * cm
    y = 18 * cm
    my_canvas.setFont('ArialBold', 17)
    my_canvas.drawCentredString(x, y, u_campaign_slogan.upper())
    print " +- set slogan"
    mapping = {'campaign_slogan':u_campaign_slogan, 'year':year}

    # print first subline
    certificate_for = translate(domain=ptt_domain,
                                    msgid='certificate_for_'+year,
                                    mapping=mapping,
                                    target_language=language,
                                    context=self)


    certificate_title = translate(
                                domain=ptt_domain,
                                msgid='certificate_title_'+year,
                                target_language=language,
                                context=self
                                )
    x = 14.85 * cm
    y = 11 * cm
    my_canvas.setFont('Arial', 32)
    my_canvas.setFillColor(HW2012BLUE)
    my_canvas.drawCentredString(x, y, certificate_title.upper())
    print " +- set Headline"#, certificate_title
    mapping = {'campaign_slogan':u_campaign_slogan, 'year':year}

    # print first subline
    certificate_for = translate(domain=ptt_domain,
                                    msgid='certificate_for_'+year,
                                    mapping=mapping,
                                    target_language=language,
                                    context=self)
    certificate_for = certificate_for.encode('utf-8')
    x = 14.85 * cm
    y = 10 * cm
    my_canvas.setFont('Arial', 18)
    my_canvas.drawCentredString(x, y, certificate_for)
    print " +- set first subline"#, certificate_for

    # print company name
    x = 14.85 * cm
    y = 7.5 * cm
    width, height = landscape(A4)
    width -= 5 * cm
    height = 10 * cm

    style = ParagraphStyle(
            name='companyName',
            fontName='Arial',
            fontSize=32,
            leading=34,
            alignment=TA_CENTER)

    company = saxutils.escape(company)
    my_canvas.setFont('Arial', 32)
    my_canvas.drawCentredString(x, y, company)
    # P = Paragraph(company, style)
    # wi, he = P.wrap(width, height)
    # P.drawOn(my_canvas, x - wi/2, y - he/2)
    print " +- set company name"#, company

    style = ParagraphStyle(
            name='ContributionHeadline',
            fontName='Arial',
            fontSize=18,
            spaceAfter=0,
            leading=22,
            alignment=1
        )

    #lines = []


    # print contribution headline
    x = 14.85 * cm
    y = 5 * cm
    width, height = landscape(A4)
    width -= 5 * cm
    height = 10 * cm

    contribution_headline = translate(domain=ptt_domain,
                                          msgid='contribution_headline_2012',
                                          mapping=mapping,
                                          target_language=language,
                                          context=self)

    contribution_headline = contribution_headline.encode('utf-8')
    my_canvas.setFont('Arial', 18)
    my_canvas.drawCentredString(x, y, contribution_headline)
    # P = Paragraph(contribution_headline, style)
    # wi, he = P.wrap(width, height)
    # P.drawOn(my_canvas, x - wi/2, y - he/2)
    print " +- set contribution headline"#, company



    # ***** FALLBACK-SOLUTION UNTIL PDFTK IS AVAILABLE *******
    if usePDFTK == 0:
        print "Set Charter-Image as second page w/o PDFTK"
        # set the webcharter-image as second page
        chartername = "charter_hw2012.jpg"
        charterfile = getattr(self, chartername , None)
        # Fallback to English
#        if not charterfile:
#            charterfile = getattr(self.charter_img, chartername % 'en')
        print "have charterfile:", [charterfile]
        # charterdata = str(charterfile._data)
        # charterdata = StringIO(charterdata)
        # charterimage = ImageReader(charterdata)
        charterimage = ImageReader(os.path.join(resources_dir, charterfilename))
        my_canvas.showPage()
        my_canvas.save()
        return acknowledge.getvalue()

    # ****** NEEDS PDFTK SUPPORT ********
    if usePDFTK == 1:
        print "Start merging with PDFTK"
        # merge the webcharter and the acknowledge PDFs
        chartername = "charter_hw2012.jpg"
        charterfile = getattr(self, chartername , None)
        # Fallback to English
#        if not charterfile:
#            charterfile = getattr(self.charter_img, chartername % 'en')
        print "got webcharter:", chartername

        # generate temp-files of both PDFs
        tmp_charter_file = tempfile.mkstemp(suffix='.pdf')
        charter_fd = open(tmp_charter_file[1], 'w')
        charter_fd.write(str(charterfile._data))
        #charter_fd.close()
        print "wrote charter-temp", tmp_charter_file[1]

        # save the acknowledge
        my_canvas.save()
        tmp_ack_file = tempfile.mkstemp(suffix='.pdf')
        ack_fd = open(tmp_ack_file[1], 'w')
        ack_fd.write(acknowledge.getvalue())
        #ack_fd.close()
        print "wrote ack-temp", tmp_ack_file[1], len(acknowledge.getvalue())

        # merge PDFs with PDF-Toolkit
        statement = 'pdftk %s %s cat output -' % (tmp_charter_file[1], tmp_ack_file[1])
        print "system-call:", statement
        ph = os.popen(statement)
        data = StringIO()
        data.write(ph.read())
        ph.close()
        print "output len:", len(data.getvalue())

        os.remove(tmp_charter_file[1])
        os.remove(tmp_ack_file[1])

        print "==================================="
        return data.getvalue()
