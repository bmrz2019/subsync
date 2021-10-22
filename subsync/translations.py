import os, builtins
from subsync import config

import logging
logger = logging.getLogger(__name__)


initialized = False


def init():
    import gettext
    gettext.install('messages', localedir=config.localedir)
    global initialized
    initialized = True

def setLanguage(language):
    import gettext, locale, importlib
    try:
        lang = language
        if lang is None:
            lang = locale.getdefaultlocale()[0].split('_', 1)[0]

        logger.info('changing translation language to %s', lang)

        if lang == 'en':
            gettext.install('messages', localedir=config.localedir)

        else:
            tr = gettext.translation('messages',
                    localedir=config.localedir,
                    languages=[lang])
            tr.install()

        global initialized
        initialized = True

        # workaround for languages being loaded before language is set
        import subsync.data.languages
        importlib.reload(subsync.data.languages)
        import subsync.data.descriptions
        importlib.reload(subsync.data.descriptions)

    except Exception as e:
        if language is None:
            logger.debug('translation language setup failed, %r', e, exc_info=False)
        else:
            logger.warning('translation language setup failed, %r', e, exc_info=False)

def listLanguages():
    try:
        langs = os.listdir(config.localedir)
    except:
        langs = []

    if 'en' not in langs:
        langs.append('en')

    return langs

def _(msg):
    if initialized:
        gettext = builtins.__dict__.get('_', None)
        if gettext is not None:
            return gettext(msg)
    return msg
