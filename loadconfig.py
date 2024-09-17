import configparser
import logging
from dotenv import dotenv_values,load_dotenv


class Config:
    def __init__(self):
        try:
            self.conffile = configparser.ConfigParser()
            logging.info("Reading ./config/mea.ini file")
            self.confcache = self.conffile.read('./config/mea.ini')
            # server
            self.SERVER_PORT = self.confcache["SERVER"]["PORT"]
            self.SERVER_HOST = self.confcache["SERVER"]["HOST"]
            self.SERVER_DEBUG = self.confcache["SERVER"]["DEBUG"]
            self.SERVER_SECRET_KEY = self.confcache["SERVER"]["SECRET_KEY"]
            # instance
            self.INST_NAMING = self.confcache["INSTANCES"]["NAMING"]
            self.INST_CUSTOM_NAME = self.confcache["INSTANCES"]["NAMING"]
            self.INST_RANDOM_NUMBER = self.confcache["INSTANCES"]["RANDOM_NUMBER"]
            self.INST_USE_SPEC_CHAR = self.confcache["INSTANCES"]["USE_SPEC_CHAR"]
            self.INST_SPEC_CHAR = self.confcache["INSTANCES"]["SPEC_CHAR"]
            # logging
            self.LOGGING_LEVEL = self.confcache["LOGGING"]["LOG_LEVEL"]
            self.LOGGING_FILE = self.confcache["LOGGING"]["LOG_FILE"]
            # default creating instance setting
            self.DEF_CPU_COUNT = self.confcache["DEFAULT"]["CPU_COUNT"]
            self.DEF_DISK_SIZE = self.confcache["DEFAULT"]["DISK_SIZE"]
            self.DEF_MEM_SIZE = self.confcache["DEFAULT"]["MEM_SIZE"]
            self.DEF_BASE_IMAGE = self.confcache["DEFAULT"]["BASE_IMAGE"]
            self.DEF_CLOUD_INIT = self.confcache["DEFAULT"]["CLOUD_INIT"]
        except configparser.Error as error:
            logging.error(error)
        except configparser.NoSectionError as sectionerror:
            logging.error(sectionerror)
        except configparser.ParsingError as parsingerror:
            logging.error(parsingerror)
        finally:
            if self.confcache is None:
                logging.info('Config file load.')
            else:
                logging.error("something gone wrong!")

    def checkEmpty(self):
        if not all([
            self.SERVER_HOST,
            self.SERVER_PORT,
            self.SERVER_DEBUG,
            self.SERVER_SECRET_KEY,
            self.INST_NAMING,
            self.INST_CUSTOM_NAME,
            self.INST_RANDOM_NUMBER,
            self.INST_USE_SPEC_CHAR,
            self.INST_SPEC_CHAR,
            self.LOGGING_LEVEL,
            self.LOGGING_FILE,
            self.DEF_CPU_COUNT,
            self.DEF_DISK_SIZE,
            self.DEF_MEM_SIZE,
            self.DEF_BASE_IMAGE,
            self.DEF_CLOUD_INIT
             ]):
            raise ValueError('Some values are empty!')
        else:
            return True

class Dotenv:
    def __init__(self):
        try:
            self.isLoadDotEnv=load_dotenv(".env")
            logging.info("Load env file successfully")
            self.envfile = dotenv_values(".env")
        except Exception as error:
            logging.error(error)
            logging.error("Start failed! The .env file could not be loaded!")
            exit()
    def appversion(self):
        return {
            "multipass_version": self.envfile["API_VERSION"]
        }
