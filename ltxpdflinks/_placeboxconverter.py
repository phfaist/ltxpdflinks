import re
import logging
logger = logging.getLogger(__name__)



_rx_placeboxurl = re.compile(r'^latexbox://', flags=re.IGNORECASE)


class LatexPlaceBoxConverter:
    def __init__(self):
        super().__init__()

    def convertLinks(self, extracted_links):
        """
        Go over URI hyperlinks, and convert those whose "protocol" in the URL is
        "latexref".

        Conversion is performed in-place, directly modifying the input object
        hierarchy.  This function doesn't return anything.

        Argument `extracted_links` is a :py:class:`ExtractedGraphicLinks` instance.
        """

        for lnk in extracted_links.links:
            if lnk.link_type == 'URI':
                uri = lnk.link_target
                m = _rx_placeboxurl.match(uri)
                if m is None:
                    continue

                # found match! Store the box reference.  We need to set a
                # special link_type for this to work.
                lnk.link_type = 'latex-box'
                lnk.link_target = uri
                
        
        # done! everything was modified in-place, so we don't return anything
        return
