
import collections
import datetime
import logging


import syncfin.db.model as mydb
import syncfin.core.config as config


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


    def update(self):
        fund_files = config.get_param('SYNCFIN_FUND_FILES')
        if not fund_files:
            return
        fund_files = [x for x in config.get_param('SYNCFIN_FUND_FILES').split(';') if x]

        for fund_file in fund_files:
            self.parse_and_save(fund_file)
