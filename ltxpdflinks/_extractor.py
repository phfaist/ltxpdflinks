import PyPDF2
import logging
logger = logging.getLogger(__name__)



class ExtractedLink:
    """
    ..........

    - `link_bbox` is relative to the page bottom left corner in user space
      units, given as `(x, y, w, h)`

    - `link_type` is one of 'URI', 'latex-ref', 'latex-cite'.  When extracting
      special types of URLs (e.g. 'latexpdf://xxx/xxx') then the extracted type
      is 'URI' with the special URI, then use a relevant SpecialLinkConverter to
      convert the special URI's to specialized types.
    """
    def __init__(self, link_bbox, link_type, link_target, **kwargs):
        super().__init__()
        x, y, w, h = link_bbox
        self.link_bbox = (float(x), float(y), float(w), float(h))
        self.link_type = link_type
        self.link_target = link_target
        self.dic = dict(kwargs)

    def __repr__(self):
        return self.__class__.__name__ + '({!r}, {!r}, {!r}, **{!r})'.format(
            self.link_bbox,
            self.link_type,
            self.link_target,
            self.dic
            )


class ExtractedGraphicLinks:
    def __init__(self, graphic_fname, size, links, *, unitlength='1bp', **kwargs):
        self.graphic_fname = graphic_fname
        self.unitlength = unitlength # LaTeX length
        (w,h) = size
        self.size = (float(w),float(h)) # (width, height)
        self.links = links
        self.dic = dict(kwargs)

    def __repr__(self):
        return self.__class__.__name__ + \
            '({!r}, {!r}, {!r}, unitlength={!r}, **{!r})'.format(
                self.graphic_fname,
                self.size,
                self.links,
                self.unitlength,
                self.dic
            )

class PdfGraphicLinksExtractor:
    def __init__(self, fname):
        super().__init__()
        self.fname = fname

    def extractGraphicLinks(self, pageno=None):
        if pageno is None:
            pageno = 0

        with open(self.fname, 'rb') as f:
            pdf = PyPDF2.PdfFileReader(f)
            page = pdf.getPage(pageno).getObject()

            page_size = (page.mediaBox.getWidth(), page.mediaBox.getHeight())

            page_bottomleft = page.mediaBox.lowerLeft

            extracted_list = []

            if '/Annots' in page:
                for annot in page['/Annots']:
                    annot = annot.getObject()
                    extracted = self._extract_annot_link(annot,
                                                         shift_rect_origin=page_bottomleft)
                    if extracted is not None:
                        logger.debug("Extracted link: %r", extracted)
                        extracted_list.append(extracted)

        return ExtractedGraphicLinks(self.fname, page_size, extracted_list)


    def _extract_annot_link(self, annot, *, shift_rect_origin=(0,0)):
        
        if '/Subtype' not in annot or annot['/Subtype'].getObject() != '/Link':
            logger.debug("Found annotation, not a link: %r", annot)
            return None

        if '/A' not in annot:
            return None

        annot_A = annot['/A'].getObject()

        if '/S' not in annot_A or annot_A['/S'].getObject() != '/URI':
            logger.warning("Link action %r has supported type (/S!=/URI)", annot_A)
            return None

        if '/URI' not in annot_A:
            logger.warning("Link action %r does not have URI", annot_A)
            return None
            
        URI = annot_A['/URI'].getObject()

        if '/Rect' not in annot:
            logger.warning("Can't get annotation's bounding box (/Rect): %r", annot)
            return None
        else:
            (x0,y0,x1,y1) = annot['/Rect'].getObject()
            x = x0 - shift_rect_origin[0]
            y = y0 - shift_rect_origin[1]
            w = x1 - x0
            h = y1 - y0
        
        return ExtractedLink(link_bbox=(x,y,w,h), link_type='URI', link_target=URI)
