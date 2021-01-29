#!/usr/bin/env python

import argparse
import threading
import time

import yfinance

import syncfin.core.record  as record
import syncfin.utils.fetch as fetch
import syncfin.recorder.wf_client as wavefront


class SyncFin(object):

    def parse_args(self):
        """
        This function parses the arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-f', '--file_tckr', nargs='+', type=str,
                            help="List of files to read tckr from.")
        parser.add_argument('-p', '--plot_tckr', action='store_true',
                            help="Plot TCKR data in Wavefront.")
        parser.add_argument('-u', '--update_tckr', action='store_true',
                            help="Update TCKR data in databse.")
        parser.add_argument('-t', '--ticker', nargs='+', type=str,
                            help="Ticker.")

        self.args = parser.parse_args()

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

        import pdb ; pdb.set_trace()
        tckrs = []
        if self.args.ticker:
            tckrs = [tckr for tckr in self.args.ticker]
        elif self.args.file_tckr:
            for fpath in self.args.file_tckr:
                try:
                    with open(fpath, 'r') as fp:
                        lines = fp.readlines()
                        lines = [x.strip() for x in lines]

                        for line in lines:
                            for tckr in line.split(' '):
                                if tckr:
                                    tckrs.append(tckr)
                except Exception as _:
                    pass

        if self.args.update_tckr:
            fetch.TickerPull().update_till_today(tckrs)

        if self.args.plot_tckr:
            for tckr in tckrs:
                self.plot(tckr)

if __name__ == '__main__':
    SyncFin().main()

