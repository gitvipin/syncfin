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


class Stock(db.Model):
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
                'fool': 'text',     # Motley fool recommendation
                'morn': 'text',     # Morning Star price
                'fair': 'text',
                'price_low': 'text',
                'price_range': 'text'
            },
            'primary_key': 'date'
            }
        ]
    }


class Events(db.Model):
    TABLE = 'events'
    DB_SCHEMA = {
        'db_name': './stocks.db',
        'tables': [{
            'name': TABLE,
            'fields': {
                'date': 'text',
                'impact': 'text',   # Impact can be a tckr or 'GLOBAL'
                },
            'primary_key': 'date'
            }
        ]
    }
