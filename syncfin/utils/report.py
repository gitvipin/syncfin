#!/usr/bin/env python

import collections

from prettytable import PrettyTable

import syncfin.db.model as mydb


class Report(object):

    def get_down_up_percent(self, closed):
        """
        Returns yesterday's price % down / up from peak / valley
        """
        last_price = float(closed[-1])
        min_price = min(closed)
        max_price = max(closed)

        down_from_peak = round((max_price - last_price) * 100 / max_price, 2)
        up_from_low = round((last_price - min_price) * 100 / min_price, 2)
        return down_from_peak, up_from_low

    def get_bear_bull_counts(self, closed):
        bulls, bears = 0, 0

        for idx, item in enumerate(closed):
            if not idx:
                continue
            if item > closed[idx -1]:
                bulls += 1
            else:
                bears += 1

        return bears, bulls

    def summary(self, tckrs, days=45):
        """
        Calculates min max of each tckr for past days.
        """
        results = collections.defaultdict(list)
        with mydb.Ticker() as db:
            for tckr in tckrs:
                db.table = tckr
                try:
                    data = db.read()
                except Exception:
                    print ("Cannot read data for .. ", tckr)
                    results[tckr] = ('-NA-', '-NA-')
                    continue
                data = data[-days:]
                closed = [float(x[4]) for x in data]
                
                down_from_peak, up_from_low = self.get_down_up_percent(closed)
                bears, bulls = self.get_bear_bull_counts(closed)
                results[tckr] = down_from_peak, up_from_low, bears, bulls

        print ("=" * 70)
        print (" " * 30, days , " days")
        print ("=" * 70)
        t = PrettyTable(['TCKR', 'Down from Peak (%)', 'Up from Low (%)', 'Bear Days', 'Bull Days'])
        for tckr, vals in sorted(results.items(), key=lambda item: item[1]):
            t.add_row([tckr, *vals])
            # t.add_row([tckr, vals[0], vals[1], vals[2], vals[3]])

        print(t)
        return results
