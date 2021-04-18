#
# Main script
#

import os
import os.path
import sys
import argparse
import logging

import colorlog


from ._extractor import ExtractedLink, ExtractedGraphicLinks, PdfGraphicLinksExtractor
from ._linkconverter import LatexRefsLinkConverter
from ._lplxexporter import LplxPictureEnvExporter
from . import __version__ as version_str


def setup_logging(level):
    # You should use colorlog >= 6.0.0a4
    handler = colorlog.StreamHandler()
    handler.setFormatter( colorlog.LevelFormatter(
        log_colors={
            "DEBUG": "white",
            "INFO": "",
            "WARNING": "red",
            "ERROR": "bold_red",
            "CRITICAL": "bold_red",
        },
        fmt={
            # emojis we can use: 🐞 🐜 🚨 🚦 ⚙️ 🧨 🧹 ❗️❓‼️ ⁉️ ⚠️ ℹ️ ➡️ ✔️ 〰️
            # 🎶 💭 📣 🔔 ⏳ 🔧 🔩 ✨ 💥 🔥 🐢 👉
            "DEBUG":    "%(log_color)s〰️    %(message)s", #'  [%(name)s]'
            "INFO":     "%(log_color)s✨  %(message)s",
            "WARNING":  "%(log_color)s⚠️   %(message)s", # (%(module)s:%(lineno)d)",
            "ERROR":    "%(log_color)s🚨  %(message)s", # (%(module)s:%(lineno)d)",
            "CRITICAL": "%(log_color)s🚨  %(message)s", # (%(module)s:%(lineno)d)",
        },
        stream=sys.stderr
    ) )

    root = colorlog.getLogger()
    root.addHandler(handler)

    root.setLevel(level)



def run_main():
    try:
        main()
    except Exception as e:
        logging.getLogger().critical("Exception: %s", e, exc_info=e)


def main(argv=None):

    parser = argparse.ArgumentParser(
        prog='ltxpdflinks',
        epilog='Have loads of fun!',
        add_help=False, # custom help option
    )

    parser.add_argument("fnames", nargs='+',
                        metavar='file',
                        help="Graphics PDF file(s) to extract links from")

    parser.add_argument("-o", "--output", dest='output_file', default=None,
                        help="Specify custom output file name where to write "
                        "the LPLX content (LaTeX commands resulting from "
                        "extracted links).  By default an .lplx file is created "
                        "with the same base file name as the input file. "
                        "This option cannot be "
                        "used when multiple input files are specified.")

    parser.add_argument("-D", "--doctex", dest='include_comments_catcode',
                        action='store_true',
                        default=False,
                        help="Include special commands for use in "
                        "package documentation files")

    parser.add_argument('-q', '--quiet', dest='verbosity', action='store_const',
                        const=logging.ERROR, default=logging.INFO,
                        help="Suppress warning messages")

    parser.add_argument('-v', '--verbose', dest='verbosity', action='store_const',
                        const=logging.DEBUG,
                        help='verbose mode')

    parser.add_argument('--version', action='version',
                        version='%(prog)s {}'.format(version_str))
    parser.add_argument('--help', action='help',
                        help='show this help message and exit')


    parsekwargs={}
    if argv is not None:
        parsekwargs.update(argv=argv)
    args = parser.parse_args(**parsekwargs)

    setup_logging(level=args.verbosity)

    logger = logging.getLogger(__name__)

    logger.info("Welcome to ltxpdflinks {version}".format(version=version_str))

    if args.output_file is not None:
        if len(args.fnames) > 1:
            raise ValueError("You cannot use -o when you specify multiple files")

    for fname in args.fnames:

        logger.debug("Extracting links from ‘%s’", fname)

        extractor = PdfGraphicLinksExtractor(fname)
        extracted = extractor.extractGraphicLinks()
        LatexRefsLinkConverter().convertLinks(extracted)

        lplxexporter = LplxPictureEnvExporter(
            include_comments_catcode=args.include_comments_catcode
        )
        exported = lplxexporter.export(extracted)

        fbasename, fext = os.path.splitext(fname)

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
            continue

        logger.info("Writing LPLX file ‘%s’", foutput)
        with open(foutput, 'w') as f:
            f.write(exported)
            continue


if __name__ == '__main__':
    run_main()
