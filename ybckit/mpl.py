import os
import time


def init():
    if 'YBC_ENV' not in os.environ or os.environ['YBC_ENV'] is None:
        pass

    import matplotlib.pyplot as plt
    import mpld3
    import protocol

    def _show():
        fig = mpld3.fig_to_dict(plt.gcf())
        request_id = protocol.send_request('python.mpld3.show', args=(), kwargs={"fig": fig})

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(0.1)
                continue

            return protocol.parse_response(raw_response)

    plt.show = _show


def cleanup():
    if 'YBC_ENV' not in os.environ or os.environ['YBC_ENV'] is None:
        pass
