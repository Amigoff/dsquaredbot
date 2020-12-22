import os
import logging
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
tok = "NzkwNTUyMTY3NjUxMzQ0Mzg1.X-CRFA.6K1AM1L088_JSP9o7Z4-J5b4sAk"
yandex_api_key = '3c39ba17-9a2c-4ba4-9e70-9f695fb7eae5'
whether_api_key = '75f6890557ef108e7ad5b23fd1acf04c'

