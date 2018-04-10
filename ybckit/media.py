# coding=utf-8
import os
import logging
import time
import wave

import pyaudio

from . import protocol
from .config import YBC_CONFIG

logger = logging.getLogger(__name__)


def record(filename=None, seconds=5, to_dir=None, rate=16000, channels=1, chunk=1024, *args, **kwargs):
    if not filename:
        return -1

    if to_dir is None:
        to_dir = './'

    if to_dir.endswith('/'):
        file_path = to_dir + filename
    else:
        file_path = to_dir + '/' + filename

    pa = pyaudio.PyAudio()

    if not YBC_CONFIG.is_under_ybc_env:
        stream = pa.open(format=pyaudio.paInt16,
                         channels=channels,
                         rate=rate,
                         input=True,
                         frames_per_buffer=chunk)

        print('* 开始录制')

        save_buffer = []
        for i in range(0, int(rate / chunk * seconds)):
            audio_data = stream.read(chunk)
            save_buffer.append(audio_data)

        print('* 结束录制')

        # stop
        stream.stop_stream()
        stream.close()
        pa.terminate()

        data = b''.join(save_buffer)
    else:
        _locals = locals()
        request_id = protocol.send_request('python.ybckit.record', (), {
            'seconds': seconds,
            'rate': rate,
            'channels': channels,
        })

        while True:
            raw_response = protocol.get_raw_response(request_id)
            if raw_response is False:
                time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
                continue

            logger.debug('request %d done' % request_id)
            file_key = protocol.parse_response(raw_response)
            full_path = "/sandbox" + file_key

            if not os.path.isfile(full_path):
                time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
                continue

            with open(full_path, 'rb') as f:
                data = f.read()
            break

    # save file
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16, ))
    wf.setframerate(rate)
    wf.writeframes(data)
    wf.close()

    return file_path


def snap():
    _locals = locals()
    request_id = protocol.send_request("python.ybckit.snap", [], {})

    while True:
        raw_response = protocol.get_raw_response(request_id)
        if raw_response is False:
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        logger.debug('request %d done' % request_id)
        file_key = protocol.parse_response(raw_response)
        full_path = "/sandbox" + file_key

        if not os.path.isfile(full_path):
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        with open(full_path) as f:
            return f.read()


def init():
    if not YBC_CONFIG.is_under_ybc_env:
        logger.debug('not under ybc env')
        return

    import ybc_speech
    ybc_speech.record = record
