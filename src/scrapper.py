#!/usr/bin/env python
'''
This module provides utilities for web scrapping the financial data.

In general data is available from: 
 - http://dev.markitondemand.com/MODApis/
 - http://finance.yahoo.com
 - http://finance.google.com 

 TODO : Make sure you are not violating any copyright.

'''
import argparse
import csv
import codecs
import urllib.request as request
import urllib.parse as parse

import sys

class SyncfinWebScrapper(object):
    def __init__(self):
        pass


class SyncfinStockScrapper(SyncfinWebScrapper):
    def __init__(self):
        pass


class SyncfinStockYahooScrapper(SyncfinWebScrapper):
    def __init__(self, tickers, fields=None):
        '''
        Scraps the financial data for symbols provided in 'tickers'. 'fields'
        is the list of parameters which are tracked. 
        '''
        self.tickers = set(tickers)     # uniquify the list. Remove duplicates.
        self.fields = None
        self.cols = None
        self.url = None

        self.build_query(tickers, fields)

    def build_query(self, tickers, fields):
        # TODO : Scan the list of fields and form the url param accodingly.
        # Check https://ilmusaham.wordpress.com/tag/stock-yahoo-data/ for the
        # symbol abbreviation.
        self.fields = None
        if not fields:
            self.fields = 'sl1rvwb4j4r5'
        # TODO : This will also have to change. 
        self.cols = '''Ticker Price PE_Ratio Volume Year_Range
                    Book_Value_per_Share EBITDA PEG_Ratio'''.split()

        self.build_url()

    def build_url(self):
        # TODO : Generalize this. This is Yahoo specific.
        url = 'http://finance.yahoo.com/d/quotes.csv?s='
        url += '+'.join(self.tickers)
        url += '&f=' + self.fields
        self.url = url

    def run(self):
        print("Fetching data from : %s" % self.url)
        req = request.urlopen(self.url)
        data = codecs.getreader('utf8')(req)
        return csv.reader(data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--stocks',
        help="Get financial data of stock(s). Use: -s 'YHOO GOOG AAPL'")

    args = parser.parse_args()

    if len(sys.argv) <=1:
        parser.print_usage()
    elif args.stocks:
        tickers = args.stocks.split()
        for row in SyncfinStockYahooScrapper(tickers).run():
            print (row)



