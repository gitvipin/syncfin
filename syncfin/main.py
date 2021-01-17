#!/usr/bin/env python

import argparse
import yfinance

import syncfin.db.model as mydb

class SyncFin(object):

    def parse_args(self):
        """
        This function parses the arguments.
        """
        parser = argparse.ArgumentParser()

        parser.add_argument('-u', '--update_tckr', nargs='+', type=str,
                            help="Update TCKR data in databse.")

        self.args = parser.parse_args()

    def update(self, tckr):
        """
        Updates 'tckr' history in local database.
        """

        _tckr  = yfinance.Ticker(tckr)

        # get historical market data
        hist_data = _tckr.history(period="max")

        with mydb.Ticker() as db:
            db.add_new_table(tckr)
            db.table = tckr
            for index, row in hist_data.iterrows():
                values = {
                    'date':  ('%s' % index).split()[0],
                    'close': round(row['Close'], 2),
                    'open': round(row['Open'], 2),
                    'high': round(row['High'], 2),
                    'low': round(row['Low'], 2),
                    'split': row['Stock Splits'],
                    'volume': int(row['Volume'])
                }
                db.write(**values)

    def main(self):
        import pdb ; pdb.set_trace()
        self.parse_args()

        if self.args.update_tckr:
            for tckr in self.args.update_tckr:
                self.update(tckr)

if __name__ == '__main__':
    SyncFin().main()

