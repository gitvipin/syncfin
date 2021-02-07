
import os
import platform
import socket


class Constants(object):
    _NAME = ''


# CONSTANTS
SYSTEM = platform.system()
LINUX_OS = True if SYSTEM == 'Linux' else False
MAC_OS = True if SYSTEM == 'Darwin' else False
WIN_OS = True if SYSTEM == 'Windows' else False


class SystemConstants(Constants):
    _NAME = "System"
    SYSTEM = SYSTEM     # Platform value.
    LINUX_OS = LINUX_OS # True if running on Linux oS
    MAC_OS = MAC_OS     # True if running on MAC OS
    WIN_OS = WIN_OS     # True if running on Windows

    # Wait for 5 seconds while joining the threads.
    THREADS_JOIN_TIMEOUT = 5


class RecorderConstants(Constants):
    _NAME = "Data Recording"
    WAVEFRONT_TRAFFIC_RECORDING = os.environ.get('WAVEFRONT_TRAFFIC_RECORDING',
                                                 True)
    WAVEFRONT_RESOURCE_RECORDING = os.environ.get('WAVEFRONT_RESOURCE_RECORDING',
                                                 True)
    # SQLITE recording configs
    SQLITE_TRAFFIC_RECORDING = os.environ.get('SQLITE_TRAFFIC_RECORDING', True)
    SQLITE_RESOURCE_RECORDING = os.environ.get('SQLITE_RESOURCE_RECORDING', True)


class WavefrontConstants(Constants):
    _NAME = "Wavefront"
    WAVEFRONT_SERVER_ADDRESS = os.environ.get('WAVEFRONT_SERVER_ADDRESS',
                                              'https://vmware.wavefront.com')
    WAVEFRONT_SERVER_API_TOKEN = os.environ.get('WAVEFRONT_SERVER_API_TOKEN', '')
    WAVEFRONT_SOURCE_TAG = os.environ.get('WAVEFRONT_SOURCE', socket.gethostname())


class SyncfinConstants(Constants):
    _NAME = "Syncfin Constants"
    SYNCFIN_FUND_FILES = os.environ.get('SYNCFIN_FUND_FILES', '')
    SYNCFIN_FUND_DIRS = os.environ.get('SYNCFIN_FUND_DIRS', '')

    SYNCFIN_ARK_EXCEL_EVENT_FILES = os.environ.get('SYNCFIN_ARK_EXCEL_EVENT_FILES', '')
    SYNCFIN_ARK_EXCEL_EVENT_DIRS = os.environ.get('SYNCFIN_ARK_EXCEL_EVENT_DIRS', '')

    SYNCFIN_ARK_MAIL_EVENT_FILES = os.environ.get('SYNCFIN_ARK_MAIL_EVENT_FILES', '')
    SYNCFIN_ARK_MAIL_EVENT_DIRS = os.environ.get('SYNCFIN_ARK_MAIL_EVENT_DIRS', '')

def get_categories():
    """
    Returns list of all the constant categories.
    """
    return [
        SystemConstants,
        RecorderConstants,
        WavefrontConstants,
        SyncfinConstants
    ]


def get_constants(categories=None):
    """
    Returns constants under the 'categories'. If not list is provided,
    returns all the constants with default values.
    """
    _categories = categories or get_categories()
    _constants = {}
    for category in _categories:
        for key, val in category.__dict__.items():
            if key.startswith('_') or not key.isupper():
                continue
            _constants[key] = val

    return _constants