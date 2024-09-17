import os
from platform import uname, processor
from psutil import cpu_count, virtual_memory, disk_usage



class OSInfo:
    def __init__(self):
        self.os = uname()
        self.commoninfo= {
            "OS":{
                "machine": self.aboutos(),
                "memory": self.totalmemory(),
                "cpu": self.cpu_info(),
                "disk": self.disk_info()
            }
        }

    def aboutos(self):
        return {
            "Platform": self.os.system,
            "Machine Name": self.os.node,
            "Release": self.os.release,
            "Version": self.os.version,
            "Architecture": self.os.machine
        }

    def totalmemory(self):
        mem = virtual_memory()
        return f"{mem.total/1024/1024:.1f}Mb"

    def cpu_info(self):
        body = {
            "Phisical Cores": cpu_count(logical=False),
            "Threads": cpu_count(logical=True)
        }
        return body

    def disk_info(self):
        return f"{disk_usage('/')/1000/1000/1000:.1f}Gb"


