import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'\xa9\x04\x13\xef;\xca\xa6u\xab\x04+J\xdf\xbbb?'

    MONGODB_SETTINGS = {"db": "UTA_Enrollment"}

