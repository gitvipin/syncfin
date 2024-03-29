#!/usr/bin/env python

import argparse
import json
import threading
import time

import yfinance

import syncfin.core.record  as record
import syncfin.utils.fetch as fetch
import syncfin.utils.report as report
import syncfin.utils.positions as positions
import syncfin.utils.events as events
import syncfin.recorder.wf_client as wavefront


class SyncFin(object):

    def parse_args(self):
        """
        This function parses the arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-a', '--ancient', action='store_true',
                            help="Update ancient/hitorical data.")
        parser.add_argument('-d', '--days', type=str,
                            help="Number of days")
        parser.add_argument('-e', '--etfs', action='store_true',
                            help="Work on ETFs.")
        parser.add_argument('-f', '--file_tckr', nargs='+', type=str,
                            help="List of files to read tckr from.")
        parser.add_argument('-g', '--groups', nargs='+', type=str,
                            help="List of Ticker groups.")
        parser.add_argument('-i', '--info', action='store_true',
                            help="Get detailed Information.")
        parser.add_argument('-p', '--plot_tckr', action='store_true',
                            help="Plot TCKR data in Wavefront.")
        parser.add_argument('-r', '--report', action='store_true',
                            help="Print report.")
        parser.add_argument('-s', '--summary', action='store_true',
                            help="Update company profile and summary.")
        parser.add_argument('-t', '--ticker', nargs='+', type=str,
                            help="Ticker.")
        parser.add_argument('-u', '--update', action='store_true',
                            help="Update TCKR data in databse.")


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

    def  _process_tckrs(self, data):
        ans = []
        if isinstance(data, str):
            ans = data.split(' ')
        elif isinstance(data, list):
            for item in data:
                ans.extend(self._process_tckrs(item))

        ans = [x.strip() for x in ans]
        ans = [x.strip(',') for x in ans]
        return ans

    def main(self):
        self.parse_args()

        tckrs = []

        if self.args.ticker:
            tckrs = [tckr for tckr in self.args.ticker]
        elif self.args.file_tckr:
            _tckrs_info = {}
            for fpath in self.args.file_tckr:
                try:
                    with open(fpath, 'r') as fp:
                        _tckrs_info.update(json.load(fp))
                except Exception as _:
                    pass

            if self.args.groups:
                invalids = []
                for group in self.args.groups:
                    if group not in _tckrs_info:
                        invalids.append(group)
                        continue
                    tckrs.extend(self._process_tckrs(_tckrs_info.get(group)['tickers']))

                if invalids:
                    print ("Invalid Group(s) : %r", invalids)
                    print ("Valid Group(s) are: %r", list(_tckrs_info.keys()))
            else:
                for group, info in _tckrs_info.items():
                    tckrs.extend(self._process_tckrs(info['tickers']))

            tckrs = [x for x in list(set(tckrs)) if x]

        days = int(self.args.days) if self.args.days else 45

        if self.args.update:
            if self.args.ancient:
                fetch.TickerPull().update_till_today(tckrs)
            if self.args.summary:
                fetch.ProfileUpdate().update_all(tckrs)
            if self.args.etfs:
                positions.Positions().update()
            if self.args.info:
                events.ARKEvents().update()

        if self.args.report:
            report.Report().summary(tckrs, days,
                                    profile=self.args.summary)
            if self.args.etfs:
                positions.Positions().report(tckrs)
            if self.args.info:
                events.ARKEvents().report(tckrs)

        if self.args.plot_tckr:
            for tckr in tckrs:
                self.plot(tckr)

if __name__ == '__main__':
    SyncFin().main()

