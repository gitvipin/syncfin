 #!/usr/bin/env python
 # 
import collections
import datetime
import logging
import yfinance

import syncfin.db.model as mydb


log = logging.getLogger(__name__)


class TickerPull(object):

    def _update_db(self, db, index, row):
        values = {
            'date':  ('%s' % index).split()[0],
            'close': round(row['Close'], 2),
            'open': round(row['Open'], 2),
            'high': round(row['High'], 2),
            'low': round(row['Low'], 2),
            'split': row.get('Stock Splits', 0),
            'volume': int(row['Volume'])
            }
        db.write(**values)

    def update(self, tckr):
        """
        Updates 'tckr' history in local database.
        """
        with mydb.Ticker() as db:
            if db.table_exists(tckr):
                db.table = tckr
                start_date = db.max('date')
                end_date = '%s' % datetime.date.today()
                data = yfinance.download(tckr,
                                 start=start_date, end=end_date)
            else:
                db.add_new_table(tckr)
                db.table = tckr
                _tckr  = yfinance.Ticker(tckr)
                # get historical market data
                data = _tckr.history(period="max")
            
            for index, row in data.iterrows():
                try:
                    self._update_db(db, index, row)
                except Exception as err:
                    log.error("Cannot process %s : %s. \nError - %r ", index, row, err)

    def update_till_today(self, tckrs):
        for tckr in tckrs:
            self.update(tckr)
