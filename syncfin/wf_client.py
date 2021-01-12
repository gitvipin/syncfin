import logging

import syncfin.config as conf

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
    event_port = conf.get_param('WAVEFRONT_PROXY_EVENT_PORT')

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
        self._testbed = conf.get_param('TESTBED_NAME')
        self._testid = str(conf.get_param('TEST_ID'))

    def write(self, record):
        if not self.enabled:
            return
        # assert isinstance(trec, ResourceRecord)
        prefix = 'syncfin.stocks.'
        tags = {"datacenter": self._testbed,
                "test_id": self._testid}
        for key, val in record.as_dict().items():
            if key in ['_id', '_timestamp']:
                continue
            metric = prefix + key
            self._client.send_metric(
                    name=metric, value=val,
                    timestamp=record.timestamp,
                    source=conf.get_param('WAVEFRONT_SOURCE_TAG'),
                    tags=tags)
