import logging
import loadconfig

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def log_level(lv):
    if lv==1:
        return logging.NOTSET
    elif lv==0:
        return logging.INFO

logging.basicConfig(format=FORMAT,
                    style = "{",
                    filemode = "a",
                    level=log_level(loadconfig.Config.LOGGING_LEVEL),
                    filename=loadconfig.Config.LOGGING_FILE)
