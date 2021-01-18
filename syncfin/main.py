#!/usr/bin/env python

import argparse
import threading
import time

import yfinance

import syncfin.core.record  as record
import syncfin.db.model as mydb
import syncfin.recorder.wf_client as wavefront


class SyncFin(object):

    def parse_args(self):
        """
        This function parses the arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--plot_tckr', nargs='+', type=str,
                            help="Plot TCKR data in Wavefront.")
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

    def plot(self, tckr):
        """
        Updates 'tckr' history in local database.
        """
        recorder = wavefront.WavefrontRecorder()
        rec = record.TickerRecord(tckr)

        # get historical market data
        _tckr  = yfinance.Ticker(tckr)
        hist_data = _tckr.history(period="max")
        for index, row in hist_data.iterrows():
            rec._timestamp = int(time.time())
            rec.date = ('%s' % index).split()[0]
            _open = round(float(row['Open']), 2)
            _close = round(float(row['Close']), 2)
            _high = round(float(row['High']), 2)
            _low = round(float(row['Low']), 2)

            rec.volatility  = round(( _high - _low) * 100 / _close, 2)
            recorder.write(rec)
            time.sleep(1)

    def main(self):
        self.parse_args()

        if self.args.update_tckr:
            for tckr in self.args.update_tckr:
                self.update(tckr)

        if self.args.plot_tckr:
            for tckr in self.args.plot_tckr:
                self.plot(tckr)

if __name__ == '__main__':
    SyncFin().main()

