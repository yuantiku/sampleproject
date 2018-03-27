import logging
import time

from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


def init():
    if not YBC_CONFIG.isUnderYbcEnv:
        logger.debug("not under ybc env")
        return

    import matplotlib.pyplot as plt
    import mpld3
    from . import protocol

    def _show():
        logger.debug("show fig by mpld3")
        fig = mpld3.fig_to_dict(plt.gcf())
        request_id = protocol.send_request('python.mpld3.show', args=(), kwargs={"fig": fig})

        logger.debug("got request_id %d" % request_id)

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(YBC_CONFIG.responseCheckInterval / 1000.0)
                continue

            logger.debug("request %d done" % request_id)
            return

    plt.show = _show
