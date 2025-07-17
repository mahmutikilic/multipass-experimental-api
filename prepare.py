import os
import shutil


class SignalSum:
    def __init__(self):
        self.MULTIPASSDIR = os.path.isdir('/snap/multipass')
        self.MULTIPASSCOMMAND = shutil.which('multipass') is not None
        self.CONFIGFILE = os.path.isfile('config/mea.ini')
        self.DOTENVFILE = os.path.isfile('.env')

    def __bool__(self):
        return all([
            self.MULTIPASSDIR,
            self.MULTIPASSCOMMAND,
            self.CONFIGFILE,
            self.DOTENVFILE,
        ])

    def multipass_ok(self):
        return {
            'multipassDirectory': self.MULTIPASSDIR,
            'multipassCommand': self.MULTIPASSCOMMAND,
        }
