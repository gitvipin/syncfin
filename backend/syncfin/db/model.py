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

    def table_name(self, tckr):
        return '_%s_' % tckr

    def add_new_table(self, tckr):
        if self.table_exists(self.table_name(tckr)):
            return
        schema = dict(self.TABLE_SCHEMA)
        schema['name'] = self.table_name(tckr)
        self.DB_SCHEMA['tables'].append(schema)
        self.create_table(schema)

    def set_table(self, tckr):
        self.table = self.table_name(tckr)


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
                'sno':'int',
                'date': 'text',
                'ticker': 'text',
                'direction': 'text',
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


class CompanyProfile(db.Model):
    """
    Holds the general information about stocks.
    Their Ticker, Motley Fool recommendation, Morning Star price range
    """
    TABLE = 'profile'
    DB_SCHEMA = {
        'db_name': './profile.db',
        'tables': [{
            'name': TABLE,
            'fields': {
                'date': 'text',
                'symbol': 'text',
                'sector': 'text',       # Sector in which it operates.
                'category': 'text',
                'industry': 'text',
                'fullTimeEmployees': 'text',     # Employee Count
                'longBusinessSummary': 'text',
                'dividend': 'text',
                'fiftyDayAverage': 'text',
                'twoHundredDayAverage': 'text',
                'totalAssets': 'text',
                'yield': 'text',
                'trailingPE': 'text',
                'averageVolume10days': 'text',
                'marketCap': 'text',
                'ytdReturn': 'text',
                'volume': 'text',
                'forwardPE': 'text',
                'profitMargins': 'text',
                'morningStarRiskRating': 'text',
                'threeYearAverageReturn': 'text',
                'lastSplitDate': 'text',
                'lastSplitFactor': 'text',
                'morningStarOverallRating': 'text',
                'earningsQuarterlyGrowth': 'text',
                'fiveYearAverageReturn': 'text'
            }
            }
        ]
    }