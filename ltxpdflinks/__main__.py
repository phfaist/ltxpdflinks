#
# Main script
#

import os
import os.path
import sys
import argparse
import logging
logger = logging.getLogger(__name__)


from ._extractor import ExtractedLink, ExtractedGraphicLinks, PdfGraphicLinksExtractor
from ._linkconverter import LatexRefsLinkConverter
from ._lplxexporter import LplxPictureEnvExporter



def main(argv=None):

    parser = argparse.ArgumentParser(prog='ltxpdflinks',
                                     epilog='Have loads of fun!')

    parser.add_argument("-o", "--output", dest='output_file', default=None,
                        help="File where to output LaTeX commands from "
                        "extracted links (default same file name but "
                        "with '.lplx' extension)")

    parser.add_argument("file", help="Graphics file to extract links from")

    parsekwargs={}
    if argv is not None:
        parsekwargs.update(argv=argv)
    args = parser.parse_args(**parsekwargs)

    extractor = PdfGraphicLinksExtractor(args.file)
    extracted = extractor.extractGraphicLinks()
    LatexRefsLinkConverter().convertLinks(extracted)
    
    exported = LplxPictureEnvExporter().export(extracted)

    fbasename, fext = os.path.splitext(args.file)

    if args.output_file is None:
        foutput = fbasename + '.lplx'
    else:
        foutput = args.output_file

    if os.path.exists(foutput) and not foutput.endswith('.lplx'):
        logger.error("Not overwriting %s (which doesn't have an .lplx extension), "
                     "please remove first", foutput)
        raise RuntimeError("Cowardly refusing to overwrite non-.lplx file %s"%(foutput))

    if foutput == '-':
        sys.stdout.write(exported)
        return

    with open(foutput, 'w') as f:
        f.write(exported)
        return


if __name__ == '__main__':
    main()
