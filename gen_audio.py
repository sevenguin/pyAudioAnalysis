"""audio generate
"""
import logging
import os
import numpy as np
from pydub import AudioSegment


def load_from_file(path):
    prefix = path.split('.')[-1]
    if prefix == 'wav':
        data = AudioSegment.from_wav(path)
    elif prefix == 'mp3':
        data = AudioSegment.from_mp3(path)
    elif prefix == 'flv':
        data = AudioSegment.from_flv(path)
    else:
        logging.warn("Wrong type of file. {}".format(path))
        data = None
    return data


def gen_by_add_louder_gaussian(path, num, base=30):
    random_states = abs(np.random.normal(0, 0.5, num))
    values = random_states[random_states <= 0.5]
    prefix = path.split('.')[-1]
    file_name = path.replace(prefix, "").strip('.')
    origin_datas = load_from_file(path)
    for i, value in enumerate(values):
        datas = origin_datas + value ** 2 * 30
        gen_file_name = '{}_{}_{}.{}'.format(file_name, 'louder', i, prefix)
        datas.export(gen_file_name, format=prefix)


def gen_by_speedup_gaussian(path, num):
    random_states = np.random.choice(np.arange(0.9, 1.1, 0.01), num)
    prefix = path.split('.')[-1]
    file_name = path.replace(prefix, "").strip('.')
    origin_datas = load_from_file(path)
    for i, value in enumerate(random_states):
        datas = origin_datas.speedup(playback_speed=value)
        gen_file_name = '{}_{}_{}.{}'.format(file_name, 'speedup', i, prefix)
        datas.export(gen_file_name, format=prefix)


if __name__ == '__main__':
    dir_path = "/Users/weill/local/opensource/pyAudioAnalysis/data/infant/dc/"
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        gen_by_add_louder_gaussian(path, 30)
        gen_by_speedup_gaussian(path, 30)
