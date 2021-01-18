import logging

import syncfin.core.config as conf

log = logging.getLogger(__name__)

try:
    from wavefront_sdk import WavefrontDirectClient, WavefrontProxyClient
except ModuleNotFoundError:
    log.warn("Wavefront package is not installed. "
             "Recording to it would be disabled.")

def _get_wf_proxy_send():
    """
    Returns Wavefront Proxy client.
    """
    host = conf.get_param('WAVEFRONT_PROXY_ADDRESS')
    if not host:
        return None

    metrics_port = conf.get_param('WAVEFRONT_PROXY_METRICS_PORT')
    distribution_port = conf.get_param('WAVEFRONT_PROXY_DISTRIBUTION_PORT')
    tracing_port = conf.get_param('WAVEFRONT_PROXY_TRACING_PORT')

    return WavefrontProxyClient(
        host=host,
        metrics_port=metrics_port,
        distribution_port=distribution_port,
        tracing_port=tracing_port)

def _get_wf_sender():
    """
    Returns Wavefront sender
    """
    # max queue size (in data points). Default: 50,000
    # batch size (in data points). Default: 10,000
    # flush interval  (in seconds). Default: 1 second

    # First try to get Wavefront Proxy client
    proxy = _get_wf_proxy_send()
    if proxy:
        return proxy

    server = conf.get_param('WAVEFRONT_SERVER_ADDRESS')
    token = conf.get_param('WAVEFRONT_SERVER_API_TOKEN')
    return WavefrontDirectClient(
        server=server, token=token)


class WavefrontRecorder(object):

    def __init__(self):
        self._client = _get_wf_sender()
        self._testbed = conf.get_param('TESTBED_NAME') or ''
        self._testid = conf.get_param('TEST_ID') or ''
        self._enabled = True
    
    @property
    def enabled(self):
        return self._enabled

    def prefix(self):
        return 

    def write(self, record):
        if not self.enabled:
            return

        prefix = 'syncfin.stocks.' + record.tckr + "."
        tags = {} # {"date": record.date}

        for key, val in record.as_dict().items():
            if key in ['_id', '_timestamp', 'date']:
                continue
            elif key.startswith('_'):
                continue
            metric = prefix + key
            self._client.send_metric(
                    name=metric, value=float(val),
                    timestamp=record.timestamp,
                    source=conf.get_param('WAVEFRONT_SOURCE_TAG'),
                    tags=tags)