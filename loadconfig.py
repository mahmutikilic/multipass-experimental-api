import configparser
from dotenv import dotenv_values, load_dotenv


class Config:
    def __init__(self, path="config/mea.ini"):
        self.parser = configparser.ConfigParser()
        self.parser.read(path)

        srv = self.parser["SERVER"]
        inst = self.parser["INSTANCES"]
        log = self.parser["LOGGING"]
        default = self.parser["DEFAULT"]

        self.SERVER_PORT = srv.getint("PORT")
        self.SERVER_HOST = srv.get("HOST")
        self.SERVER_DEBUG = srv.getboolean("DEBUG")
        self.SERVER_SECRET_KEY = srv.get("SECRET_KEY")

        self.INST_NAMING = inst.getint("NAMING")
        self.INST_CUSTOM_NAME = inst.get("CUSTOM_NAME")
        self.INST_RANDOM_NUMBER = inst.getint("RANDOM_NUMBER")
        self.INST_USE_SPEC_CHAR = inst.getint("USE_SPEC_CHAR")
        self.INST_SPEC_CHAR = inst.get("SPEC_CHAR")

        self.LOG_LEVEL = log.get("LOG_LEVEL")
        self.LOG_FILE = log.get("LOG_FILE")

        self.DEF_CPU_COUNT = default.getint("CPU_COUNT")
        self.DEF_DISK_SIZE = default.get("DISK_SIZE")
        self.DEF_MEM_SIZE = default.get("MEM_SIZE")
        self.DEF_BASE_IMAGE = default.get("BASE_IMAGE")
        self.DEF_CLOUD_INIT = default.get("CLOUD_INIT")

    def check_empty(self):
        for section in self.parser.sections():
            for key, value in self.parser[section].items():
                if value == "":
                    raise ValueError(f"{key} is empty")
        return True


class Dotenv:
    def __init__(self, path=".env"):
        load_dotenv(path)
        self.envfile = dotenv_values(path)

    def appversion(self):
        return {"multipass_version": self.envfile.get("API_VERSION", "")}

