
import uuid

class Record(object):

    def __init__(self):
        self._id = '%s' % uuid.uuid4()
        self._timestamp = None

    @property
    def id(self):
        return self._id

    @property
    def timestamp(self):
        return self._timestamp

    def __str__(self):
        return '%r' % self.__dict__

    def as_dict(self):
        return self.__dict__


class TickerRecord(Record):

    def __init__(self, tckr=None):
        super(TickerRecord, self).__init__()
        self._tckr = tckr

    @property
    def tckr(self):
        return self._tckr