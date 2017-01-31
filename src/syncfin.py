#!/usr/bin/env python

import argparse

import config as config

class SyncFin(object):
    def __init__(self):
        self.args = None
        self.config = config.SyncfinConfig()

    def parse_args(self):
        """
        This function parses the arguments.
        """
        parser = argparse.ArgumentParser()

        parser.add_argument('-c', '--config', action="store_true",
                            help="Print configurations.")

        parser.add_argument('-i', '--intrinsic_value',
                            help="Get Intrinsic value of stock(s)")

        self.args = parser.parse_args()

    def main(self):
        self.parse_args()

        if self.args.config:
            self.config.print_me()

        if self.args.intrinsic_value:
            print "Calculating Intrinsic Value for ", self.args.intrinsic_value

if __name__ == '__main__':
    SyncFin().main()

