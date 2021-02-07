
import collections
import datetime
import logging
import os

import xlrd

import syncfin.db.model as mydb
import syncfin.core.config as config

from prettytable import PrettyTable

log = logging.getLogger(__name__)


class Events(object):
    SYNCFIN_EVENT_FILES_CONST = ''
    SYNCFIN_EVENT_DIRS_CONST = ''

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
        event_files = config.get_param(self.SYNCFIN_EVENT_FILES_CONST)
        if not event_files:
            return
        event_files = [x for x in event_files.split(';') if x]

        for event_file in event_files:
            self._update_from_file(event_file)

    def _update_from_dirs(self):
        event_dirs = config.get_param(self.SYNCFIN_EVENT_DIRS_CONST)
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


class ARKExcelEvents(Events):
    SYNCFIN_EVENT_FILES_CONST = 'SYNCFIN_ARK_EXCEL_EVENT_FILES'
    SYNCFIN_EVENT_DIRS_CONST = 'SYNCFIN_ARK_EXCEL_EVENT_DIRS'

    def parse_and_save(self, fpath):
        """
        Parses ARK daily trades file and saves it to Events
        Database.
        """

        workbook = xlrd.open_workbook(fpath, ignore_workbook_corruption=True)
        sheet = workbook.sheet_by_name("Sheet1")

        # Header is typically like this
        # ['FUND', 'Date', 'Direction', 'Ticker', 'CUSIP', 'Name', 'Shares', '% of ETF']
        header = sheet.row_values(3)

        data = []

        for row in range(4, sheet.nrows):
            data.append(sheet.row_values(row))

        etfIdx = header.index('FUND')
        dateIdx = header.index('Date')
        dirIdx = header.index('Direction')
        tckrIdx = header.index('Ticker')
        compIdx = header.index('Name')
        weightIdx = header.index('% of ETF')


        with mydb.EventsDB() as _db:
            _db.table = _db.TABLE
            try:
                sno = int(_db.max('sno') or 1)
            except ValueError:
                sno = 0

            for line in data:
                try:
                    date = line[dateIdx].strip()
                    ticker = line[tckrIdx].strip()
                    etf = line[etfIdx].strip()
                    direction = line[dirIdx].strip()
                    company = line[compIdx].strip()
                    weight = line[weightIdx]
                    remark = '%s - %s(%s) - %s %% .' % (
                            direction, ticker, company, weight
                    )
                    if _db.read(date=date, direction=direction, etf=etf, remarks=remark):
                        # If entry is already present for a ticker in a fund on a given date,
                        # do not create duplicate entry and ignore it.
                        continue
                    sno += 1
                    _db.write(sno=sno,
                              date=date,
                              ticker=ticker,
                              etf=etf,
                              direction=direction,
                              analyst='ARK',
                              remarks=remark)

                except Exception as err:
                    log.info("Skipped line : %s", line)
                    log.error('%r' % err)


class ARKMailEvents(Events):
    SYNCFIN_EVENT_FILES_CONST = 'SYNCFIN_ARK_MAIL_EVENT_FILES'
    SYNCFIN_EVENT_DIRS_CONST = 'SYNCFIN_ARK_MAIL_EVENT_DIRS'

    def parse_and_save(self, fpath):
        """
        Parses ARK daily trades file and saves it to Events
        Database.
        """
        data = []

        try:
            with open(fpath, 'r') as fp:
                data = fp.readlines()
                data = [x.strip() for x in data]
        except Exception:
            log.error("Error in reading file %s", fpath)
            return

        header = ['S No', 'Fund', 'Date', 'Direction', 'Ticker', 'CUSIP',
                  'Company', 'Shares', '% of ETF']
        
        import pdb ; pdb.set_trace()
        etfIdx = header.index('Fund')
        dateIdx = header.index('Date')
        dirIdx = header.index('Direction')
        tckrIdx = header.index('Ticker')
        compIdx = header.index('Company')
        sharesIdx = header.index('Shares')
        weightIdx = header.index('% of ETF')

        with mydb.EventsDB() as _db:
            _db.table = _db.TABLE
            try:
                sno = int(_db.max('sno') or 1)
            except ValueError:
                sno = 0

            for line in data:
                try:
                    line = line.split('\t')
                    if all([x in line for x in header[1:-1] ]):
                        continue
                    ticker = line[tckrIdx].strip()
                    etf = line[etfIdx].strip()
                    direction = line[dirIdx].strip()
                    company = line[compIdx].strip()
                    weight = line[weightIdx]
                    shares = line[sharesIdx]
                    remark = '%s - %s(%s) - %s shares- %s %% weigth.' % (
                            direction, ticker, company, shares,  weight
                    )
                    date = line[dateIdx].strip()
                    date = '-'.join(date.split('/')[::-1])
                    if _db.read(date=date, direction=direction, etf=etf, remarks=remark):
                        # If entry is already present for a ticker in a fund on a given date,
                        # do not create duplicate entry and ignore it.
                        continue
                    sno += 1
                    _db.write(sno=sno, date=date, ticker=ticker, etf=etf,
                              direction=direction, analyst='ARK', remarks=remark)
                except Exception as err:
                    log.info("Skipped line : %s", line)
                    log.error('%r' % err)
                    continue


class ARKEvents(object):

    def update(self):
        ARKExcelEvents().update()
        ARKMailEvents().update()

    def report(self, tickers):
        results = collections.defaultdict(list)
        with mydb.EventsDB() as _db:
            _db.table = _db.TABLE

            for ticker in tickers:
                records = _db.read(ticker=ticker)
                results[ticker].extend(sorted(records))

        t = PrettyTable(['S. No.','Date', 'Ticker', 'Direction', 'ETF', 'Analyst', 'Remarks'])

        print ("=" * 55)
        print (" " * 20, " Events ")
        print ("=" * 55)
        for ticker in sorted(results):
            for holding in results[ticker]:
                t.add_row(holding)

        print(t)