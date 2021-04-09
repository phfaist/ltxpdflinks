import re
import logging
logger = logging.getLogger(__name__)

import urllib.parse


_rx_latexrefurl = re.compile(r'^latexref://(?P<ref_type>ref|cite)/(?P<ref_target>.*)$',
                             flags=re.IGNORECASE)


class LatexRefsLinkConverter:
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
                m = _rx_latexrefurl.match(uri)
                if m is None:
                    continue
                # found match! change link type.
                ref_type, ref_target = m.group('ref_type'), m.group('ref_target')
                ref_target = urllib.parse.unquote(ref_target)
                if ref_type == 'ref':
                    lnk.link_type = 'latex-ref'
                    lnk.link_target = ref_target
                    continue
                if ref_type == 'cite':
                    lnk.link_type = 'latex-cite'
                    lnk.link_target = ref_target
                    continue
                
                logger.warning("Unsupported ref_type in special URL %r", uri)
        
        # done! everything was modified in-place, so we don't return anything
        return
