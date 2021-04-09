#
# ltxpdflinks package
#

import PyPDF2


class ExtractedLink:
    def __init__(self, **kwargs):
        super().__init__()
        self.dic = dict(kwargs)


class PdfLinksExtractor:
    def __init__(self, fname):
        super().__init__()
        self.fname = fname

    def extract_links(self):
        with open(self.fname, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            for pgnum in range(pdf.getNumPages()):
                page = pdf.getPage(pgnum).getObject()
                for annot in page['/Annots']:
                    annot = annot.getObject()
                    print('*', annot)
                    print('\t/A ->', annot['/A'].getObject())
                    print('\t\tURI = ', annot['/A']['/URI'].getObject())
                    print('')
