
import collections
import datetime
import logging
import os


import syncfin.db.model as mydb
import syncfin.core.config as config

from prettytable import PrettyTable

log = logging.getLogger(__name__)


class Events(object):

    def parse_and_save(self, fpath):
        """
        Parses the file and saves to Positions DB.
        """

        data = []
        with open(fpath, 'r') as fp:
            data = fp.readlines()
            data = [_.strip() for _ in data]
            data = [x for x in data if not x.startswith('#')]

        with mydb.EventsDB() as _db:
            _db.table = _db.TABLE
            for line in data[1:]:
                try:
                    sno , date, ticker, etf, analyst, remarks = line.split(',')
                    if _db.read(sno=sno):
                        # If entry is already present for a ticker in a fund on a given date,
                        # do not create duplicate entry and ignore it.
                        continue
                    _db.write(sno=sno.strip(),
                              date=date.strip(),
                              ticker=ticker.strip(),
                              etf=etf.strip(),
                              analyst=analyst.strip(),
                              remarks=remarks.strip())

                except Exception as err:
                    log.info("Skipped line : %s", line)
                    log.error('%r' % err)

    def _update_from_file(self, event_file):
            try:
                self.parse_and_save(event_file)
            except Exception as _:
                log.error("Error in updating - %s", event_file)

    def _update_from_files(self):
        event_files = config.get_param('SYNCFIN_EVENT_FILES')
        if not event_files:
            return
        event_files = [x for x in event_files.split(';') if x]

        for event_file in event_files:
            self._update_from_file(event_file)

    def _update_from_dirs(self):
        event_dirs = config.get_param('SYNCFIN_EVENT_DIRS')
        if not event_dirs:
            return

        event_dirs = [x for x in event_dirs.split(';') if x]
        # Add info from all the files in directory.
        for event_dir in event_dirs:
            for root, _, files in os.walk(event_dir):
                for fpath in files:
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
        with mydb.EventsDB() as _db:
            _db.table = _db.TABLE

            for ticker in tickers:
                records = _db.read(ticker=ticker)
                results[ticker].extend(sorted(records))

        t = PrettyTable(['S. No.','Date', 'Ticker', 'ETF', 'Analyst', 'Remarks'])

        print ("=" * 55)
        print (" " * 20, " Events ")
        print ("=" * 55)
        for ticker in sorted(results):
            for holding in results[ticker]:
                t.add_row(holding)

        print(t)
