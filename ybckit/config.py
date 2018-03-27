import os


class YbcConfig:
    isUnderYbcEnv = False

    requestFile = None

    responseFilePrefix = None

    responseCheckInterval = 100.0

    def __init__(self):
        self.reload()

    def reload(self):
        if 'YBC_ENV' in os.environ:
            self.isUnderYbcEnv = True

        if 'YBC_REQUEST_FILE' in os.environ:
            self.requestFile = os.environ['YBC_REQUEST_FILE']

        if 'YBC_RESPONSE_FILE_PREFIX' in os.environ:
            self.responseFilePrefix = os.environ['YBC_RESPONSE_FILE_PREFIX']

        if 'YBC_RESPONSE_CHECK_INTERVAL' in os.environ:
            self.responseCheckInterval = float(os.environ['YBC_RESPONSE_CHECK_INTERVAL'])


YBC_CONFIG = YbcConfig()
