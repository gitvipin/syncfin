
import collections
import datetime
import logging
import os


import syncfin.db.model as mydb
import syncfin.utils.common as common
import syncfin.core.config as config

from prettytable import PrettyTable

log = logging.getLogger(__name__)


class Positions(object):

    def parse_and_save(self, fpath):
        """
        Parses the file and saves to Positions DB.
        """

        data = []
        with open(fpath, 'r') as fp:
            data = fp.readlines()
            data = [_.strip() for _ in data]

        with mydb.PositionsDB() as _db:
            _db.table = _db.TABLE
            for line in data[1:]:
                try:
                    date, fund, company, ticker, _, shares, mvalue, weight = line.split(',')
                    # TODO: Convert date to standard format.
                    date = '-'.join(date.split('/')[::-1])

                    if _db.read(date=date, fund=fund, ticker=ticker):
                        # If entry is already present for a ticker in a fund on a given date,
                        # do not create duplicate entry and ignore it.
                        continue
                    _db.write(date=date,
                            fund=fund,
                            company=company,
                            ticker = ticker,
                            shares = shares,
                            mvalue = mvalue,
                            weight = weight
                        )
                except Exception as err:
                    log.info("Skipped line : %s", line)
                    log.error('%r' % err)

    def _update_from_file(self, fund_file):
            try:
                self.parse_and_save(fund_file)
            except Exception as _:
                log.error("Error in updating - %s", fund_file)

    def _update_from_files(self):
        fund_files = config.get_param('SYNCFIN_FUND_FILES')
        if not fund_files:
            return
        fund_files = [x for x in fund_files.split(';') if x]

        for fund_file in fund_files:
            self._update_from_file(fund_file)

    def _update_from_dirs(self):
        funds_dirs = config.get_param('SYNCFIN_FUND_DIRS')
        if not funds_dirs:
            return

        funds_dirs = [x for x in funds_dirs.split(';') if x]
        # Add info from all the files in directory.
        for funds_dir in funds_dirs:
            for root, _, files in os.walk(funds_dir):
                for fpath in files:
                    if fpath.startswith('.'):
                        continue
                    self._update_from_file(os.path.join(root, fpath))

    def update(self):
        """
        Update database from CSV files of respective ETFs.
        ETFs must be in ./data/sample_etf.csv format.
        """
        self._update_from_files()
        self._update_from_dirs()

    def report(self, tickers):
        results = collections.defaultdict(list)
        with mydb.PositionsDB() as _db:
            _db.table = _db.TABLE

            for ticker in tickers:
                records = _db.read(ticker=ticker)
                results[ticker].extend(sorted(records))

        t = PrettyTable(['Date','Fund','Company','Ticker','Shares',
                         'Market value($) of holding', 'Weight(%)', 'Note'])

        print ("=" * 70)
        print (" " * 30, " Holdings (in ETFs) ")
        print ("=" * 70)
        for ticker in sorted(results):
            for holding in results[ticker]:
                holding = list(holding)
                holding[5] = common.format_currency(holding[5])
                t.add_row(holding)

        print(t)
