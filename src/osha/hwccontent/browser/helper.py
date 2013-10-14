from Products.Five import BrowserView
from zope.interface import implements
from zope.interface import Interface

class IHelperView(Interface):
    """ """
    
    def break_in_lines():
        """ sets the views on all folders """


class HelperView(BrowserView):
    """ Helper View to manage the campaign site setup """
    implements(IHelperView)

    def __init__(self, context, request=None):
        self.context = context

    def break_in_lines(self, text, max_width=20):
        """ tries to add a break after a number of chars """
        arr = []
        while (text!=''):
            if len(text) < max_width:
                arr.append(text)
                text = ''

            space = text.rfind(u' ', 0, max_width)
            if space == -1:
                arr.append(text)
                text = ''

            arr.append(text[:space])
            text = text[space:]


        carr = [x for x in arr if x.strip() != '']

        text = "<br/>".join(carr)
        lines = len(carr)

        return (lines, text)
