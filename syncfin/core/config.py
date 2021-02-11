
import logging

import syncfin.core.consts as consts 


log = logging.getLogger(__name__)
configs = None


class Config(object):
    BOOLS = ('TRUE', 'FALSE')
    NAME = "CONFIG"

    def __init__(self, db_file=None):
        # set params
        self._params = {}

        # Initialize params as default.
        self._set_defaults()

    def _set_defaults(self):
        """
        Initialized params with default constants.
        """
        for param, val in consts.get_constants().items():
            if str(val).upper() in self.BOOLS:
                val = True if str(val).upper() == "TRUE" else False
            self._params[param] = val

    def get_param(self, param):
        """
        Return the value of a config param. Param is always
        returned from local cache as it is simply a reflector of database file.
        """
        return self._params.get(param, None)

    def set_param(self, param, val, write_to_db=True):
        self._params[param] = val


def get_configs():
    global configs
    if not configs:
        configs = Config()

    return configs


def get_param(param, default=None):
    return get_configs().get_param(param) or default


def set_param(param, val):
    return get_configs().set_param(param, val)