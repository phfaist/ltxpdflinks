#
# Main script
#

import sys
import argparse


def main(argv):

    parser = argparse.ArgumentParser(prog='ltxpdflinks',
                                     epilog='Have loads of fun!')

    parser.add_argument("file",
                        help="File to extract links from")

    parser.add_argument("-o, --output", dest='output_file',
                        help="File where to output LaTeX commands from "
                        "extracted links (default '-' which means stdout)")

    args = parser.parse_args(argv)

    print("IMPLEMENT ME! {!r}".format(args))




if __name__ == '__main__':
    main(sys.argv)
