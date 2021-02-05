#!/usr/bin/env python
from sql30 import db


class Ticker(db.Model):
    TABLE = 'AAPL'
    DB_SCHEMA = {
        'db_name': './ticker.db',
        'tables': []
        }
    VALIDATE_BEFORE_WRITE = True

    TABLE_SCHEMA = {
        'name': TABLE,
        'fields': {
            'date': 'text',
            'open': 'text',
            'high': 'text',
            'low': 'text',
            'close': 'text',
            'volume' : 'int',
            'split' : 'text'
            },
        'primary_key': 'date'
        }

    def __init__(self, *args, **kwargs):
        super(Ticker, self).__init__(*args, **kwargs)
        self.fetch_schema()

    def add_new_table(self, tckr):
        if self.table_exists(tckr):
            return
        schema = {k: v for k, v in self.TABLE_SCHEMA.items()}
        schema['name'] = tckr
        self.DB_SCHEMA['tables'].append(schema)
        self.create_table(schema)


class PositionsDB(db.Model):
    """
    Holds the information on a Ticker about how much position
    an ETF is holding in the ticker.
    """
    TABLE = 'positions'
    DB_SCHEMA = {
        'db_name': './positions.db',
        'tables': [{
            'name': TABLE,
            'fields': {
                'date': 'text',
                'fund': 'text',
                'company': 'text',
                'ticker': 'text',
                'shares': 'text',
                'mvalue': 'text',
                'weight': 'text',
                'note': 'text',
            }
            }
        ]
    }

class EventsDB(db.Model):
    """
    Holds the events on a Ticker. Event can be coming from Buy / Sell
    of a stock tcker from an ETF or can be manually entered.
    """
    TABLE = 'events'
    DB_SCHEMA = {
        'db_name': './events.db',
        'tables': [{
            'name': TABLE,
            'fields': {
                'sno':'text',
                'date': 'text',
                'ticker': 'text',
                'etf': 'text',
                'analyst': 'text',
                'remarks': 'text',   # Impact can be a tckr or 'GLOBAL'
                },
            'primary_key': 'sno'
            }
        ]
    }


class StockInfo(db.Model):
    """
    Holds the general information about stocks.
    Their Ticker, Motley Fool recommendation, Morning Star price range
    """
    TABLE = 'general'
    DB_SCHEMA = {
        'db_name': './stocks.db',
        'tables': [{
            'name': TABLE,
            'fields': {
                'tckr': 'text',
                'date': 'text',     # Motley fool recommendation
                'morn': 'text',     # Morning Star price
                'fair': 'text',
                'price_low': 'text',
                'price_range': 'text'
            },
            'primary_key': 'date'
            }
        ]
    }