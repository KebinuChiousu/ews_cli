#!/usr/bin/python3

import sys
import argparse
from . import ews


def main():
    """ Parse cli args and invoke main program """
    parser = argparse.ArgumentParser(
        description=('Outlook Web Access CLI Client'))
    parser.add_argument('-d', '--daemon',
                        required=False, action='store_true',
                        help='Run non-interactive')

    args = parser.parse_args()

    ews.ExchangeWebAccess(args)


if __name__ == "__main__":
    sys.exit(main())
