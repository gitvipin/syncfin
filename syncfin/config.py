#!/usr/bin/env python

'''
This module handles the configuration read/write.
'''
import ConfigParser


class SyncfinConfig(object):
    CONFIG_FILE_PATH = '../data/config.ini'

    def __init__(self, config_path=None):
        self.config = ConfigParser.ConfigParser()
        self.config.optionxform = str

        # Read the configuration file.
        cfgpath = self.CONFIG_FILE_PATH if config_path is None else config_path
        self.config.read(cfgpath)

        # Fetch the sections from the config file.
        self.sections = self.config.sections()
        if self.config.has_section('DEFAULT'):
            self.sections.extend('DEFAULT')

    def print_me(self):
        print ("\n\nConfiguration:")
        print ("-" * 30)
        for section in self.sections:
            print ("\n[ %s ]" % section)
            for option in self.config.options(section):
                print ("%s = %s" % (option, self.config.get(section, option)))

        print ("\n")

_params = {}

def get_param(param):
    """
    """
    return _params.get(param, None)

def set_param(param, val):
    """
    """
    _params[param] = val

set_param['TESTBED_NAME'] = 'SYNCFIN'
set_param['TEST_ID'] ='SYNCFIN'

if __name__ == '__main__':
    SyncfinConfig().print_me()
