#!/usr/bin/python3

import sys
import argparse
from ews_cli import ews

def main():
    parser = argparse.ArgumentParser(description=('Outlook Web Access CLI Client'))
    parser.add_argument('-d', '--daemon', required=False, action='store_true', help='Run non-interactive')

    args = parser.parse_args()

    ews.exchange_web_access(args)

if __name__ == "__main__":
    sys.exit(main())
