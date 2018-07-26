# coding=utf-8
import logging
import os
import random
import string
import time
import wave

import ybc_speech
import ybc_camera

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

    logger.debug('save file path: %s' % file_path)

    if not YBC_CONFIG.is_under_ybc_env:
        import pyaudio

        pa = pyaudio.PyAudio()

        stream = pa.open(format=pyaudio.paInt16,
                         channels=channels,
                         rate=rate,
                         input=True,
                         frames_per_buffer=chunk)

        logger.info('* 开始录制')

        save_buffer = []
        for i in range(0, int(rate / chunk * seconds)):
            audio_data = stream.read(chunk)
            save_buffer.append(audio_data)

        logger.info('* 结束录制')

        # stop
        stream.stop_stream()
        stream.close()
        pa.terminate()

        data = b''.join(save_buffer)

        # save file
        wf = wave.open(file_path, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16, ))
        wf.setframerate(rate)
        wf.writeframes(data)
        wf.close()
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
            logger.debug('file_key: %s' % file_key)
            os.rename(file_key, file_path)

            return file_path


def snap(filename=None):
    if filename:
        file_path = './' + filename

    _locals = locals()
    request_id = protocol.send_request("python.ybckit.snap", [], {})

    while True:
        raw_response = protocol.get_raw_response(request_id)
        if raw_response is False:
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        logger.debug('request %d done' % request_id)
        file_key = protocol.parse_response(raw_response)
        logger.debug('file_key: %s' % file_key)
        if filename:
            os.rename(file_key, file_path)

        if filename:
            return filename
        else:
            return file_key


def play(filename):
    _locals = locals()
    request_id = protocol.send_request("python.ybckit.play", [], {"filename": filename})

    while True:
        raw_response = protocol.get_raw_response(request_id)
        if raw_response is False:
            time.sleep(YBC_CONFIG.response_check_interval / 1000.0)
            continue

        logger.debug('request %d done' % request_id)
        return


def speak(text='', model_type=2):
    if text:
        filename = '_____temp/speak_%s.wav' % ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        filename = ybc_speech.text2voice(text, filename, model_type)
        play(filename)


def init():
    if not YBC_CONFIG.is_under_ybc_env:
        logger.debug('not under ybc env')
        return

    ybc_speech.record = record
    ybc_speech.speak = speak
    ybc_camera.camera = snap
