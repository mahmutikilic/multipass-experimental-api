import logging
from loadconfig import Config,Dotenv
import logg3r
import os

class SignalSum:
    def __init__(self):
        logging.info("getting all check status about os and commands requirements")
        if self.__bool__() is False:
            exit(1)
    def sign4ls(self):
        self.MULTIPASSDIR =Checkmultipass.findMultipassDir()
        self.MULTIPASSCOMMAND = Checkmultipass.checkMultipassCommand()
        self.ACCECIBILITYMULTIPASSCOMMAND = Checkmultipass.checkAbilityRunCommand()
        self.CONFIGFILE = CheckConfig.checkConfig()
        self.CONFIGVALUES = Config.checkEmpty()
        self.DOTENVFILE = Dotenv.isLoadDotEnv

    def __bool__(self):
        return all(
                [
                    self.MULTIPASSDIR and \
                    self.MULTIPASSCOMMAND and \
                    self.ACCECIBILITYMULTIPASSCOMMAND and \
                    self.MULTIPASSDIR and \
                    self.MULTIPASSCOMMAND and \
                    self.ACCECIBILITYMULTIPASSCOMMAND and \
                    self.DOTENVFILE
                ]
            )

    def multipassOk(self):
        return {
            "multipassDirectory": self.MULTIPASSDIR,
            "multipassCommand": self.MULTIPASSCOMMAND,
            "multipassAbility": self.ACCECIBILITYMULTIPASSCOMMAND
        }

class Checkmultipass:
    def __init__(self):
        logging.info("the multipass check for directory and command.")
    def findMultipassDir(self):
        if os.path.isdir('/snap/multipass'):
            logging.info("the multipass directory is present.")
            return True
        else:
            logging.fatal('Multipass directory not found! API could\'t start')
            return False

    def checkMultipassCommand(self):
        if os.path.isfile("/snap/bin/multipass"):
            logging.info("the multipass command is present.")
            return True
        else:
            logging.fatal("Multipass command not found! API could\'t start")

    def checkAbilityRunCommand(self):
        try:
            stdout = os.system(command="multipass info")
            assert "Command 'multipass' not found" in stdout or \
                "Multipass: not found" in stdout or \
                "No such file or directory: 'multipass'" in stdout
            logging.info("Multipass command is accessibility ")
            return False
        except AssertionError :
            logging.fatal("Multipass command is not accessible")
            return True

class CheckConfig:
    def __init__(self):
        logging.info("the config check.")
    def checkConfig(self):
        if os.path.isfile("./config/mea.ini"):
            return True
        else:
            logging.fatal("Config file not found! Settings can\'t set")
            exit(1)

    def checkEnv(self):
        if os.path.isfile("./.env"):
            return True
        else:
            logging.warning("Environment file not found! Could\'t get version info")
            return False

