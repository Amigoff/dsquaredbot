import os
import logging
from random import choice

basedir = os.path.abspath(os.path.dirname(__file__))


LOG_LEVEL = logging.INFO
DEBUG = False
TESTING = False
CSRF_ENABLED = True
SECRET_KEY = 'this-really-needs-to-be-changed'

LOG_FORMAT = "%(log_color)s %(asctime)s %(name)s-%(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
LOG_NAME_FORMAT = "%Y-%m-%d.log"

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
OPUS_LIBS = ['libopus.so.0.5.3', 'libopus-0.x86.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

NAME = 'аллах'
tok = "NzAyMTM5MjM5MTIyNDY4OTc0.Xp7sHw.tb7X4XSUcMthvgiVEz_7hN1Vrn0"
yandex_api_key = '3c39ba17-9a2c-4ba4-9e70-9f695fb7eae5'
whether_api_key = '75f6890557ef108e7ad5b23fd1acf04c'


class Phrases(object):

    def get_phrase_playing_music(self, state, queue_len=0):
        """
        Возвращает фразу при проигрывании музыки
        :param state: Состояние, принимает значения "ok"/"queue"/"error"
        """
        _phrases = {'ok': ['Сделаю, дорогой', "Да... Хорошая песня, ставлю сиюминутно!", "*Ставит новую пластинку*",
                           "Ежжи, будет сделано", "Всё для тебя... Включаю"],
                    'queue': [f'Брат, тут очередь, добавил твой трек. \nДлина очереди: {queue_len}',
                              f"Добавлено в очередь\nДлина очереди: {queue_len}",
                              f"А не много вы мне запросов дали?\nДобавлено в очередь\nДлина очереди: {queue_len}",
                              f"Добавлено в очередь\nДлина очереди: {queue_len}",
                              f"Скоро сыграю ;)\nДобавлено в очередь\nДлина очереди: {queue_len}",
                              f"Добавлено в очередь\nДлина очереди: {queue_len}"],
                    'error': ['Аллах разгневался... Не могу поставить эту песню. (Ошибка воспроизведения)']
                    }
        return choice(_phrases.get(state, []))


COLOR_YELLOW = 0xFFC300
COLOR_GREEN = 0x2ECC71
COLOR_BLUE = 0x3498DB
COLOR_RED = 0xC70039