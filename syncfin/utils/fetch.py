 #!/usr/bin/env python
 # 
import collections
import datetime
import logging
import yfinance

import syncfin.db.model as mydb
import syncfin.utils.parallel as parallel


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
            if db.table_exists(db.table_name(tckr)):
                db.set_table(tckr)
                start_date = db.max('date')
                end_date = '%s' % datetime.date.today()
                if start_date == end_date:
                    return  # Nothing to update.
                data = yfinance.download(tckr,
                                 start=start_date, end=end_date)
            else:
                db.add_new_table(tckr)
                db.set_table(tckr)
                _tckr  = yfinance.Ticker(tckr)
                # get historical market data
                data = _tckr.history(period="max")
            
            for index, row in data.iterrows():
                try:
                    self._update_db(db, index, row)
                except Exception as err:
                    if 'UNIQUE constraint failed' in err.args[0]:
                        # Trying to update for same date again.
                        continue
                    elif 'cannot convert float NaN to integer' in err.args[0]:
                        continue
                    log.error("Cannot process %s : %s. \nError - %r ", index, row, err)

    def update_till_today(self, tckrs):
        print ("Updating Historical data for : %s" %  ' '.join(tckrs))
        for tckr in tckrs:
            try:
                self.update(tckr)
                print("%s ... Done" % tckr)
            except Exception as _:
                print("%s ... Skipped due to error" % tckr)


class ProfileUpdate(object):

    def update(self, tckr):
        with mydb.CompanyProfile() as db:
            db.table = db.TABLE
            info = yfinance.Ticker(tckr).info

            values = {}
            for field in db._get_fields(db.TABLE):
                if field == 'date':
                    continue
                try:
                    val = info.get(field, '')
                    if val:
                        values[field] = val
                except Exception:
                    pass    # ignore fields which are not available.

            values['date'] = datetime.datetime.today().strftime('%Y-%m-%d')
            db.write(**values)

    def _update(self, tckr):
        try:
            self.update(tckr)
            log.info("%s (Summary) ... Done" % tckr)
        except Exception as _:
            log.info("%s ... Skipped due to error" % tckr)

    def update_all(self, tckrs):
        print ("Updating Profile data for : %s" %  ' '.join(tckrs))
        params = [(tckr, (tckr,) , {}) for tckr in tckrs]
        parallel.ThreadPool(self._update, params)
