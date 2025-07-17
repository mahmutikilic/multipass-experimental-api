from platform import uname
from psutil import cpu_count, virtual_memory, disk_usage


class OSInfo:
    def __init__(self):
        self.os = uname()
        self.commoninfo = {
            "OS": {
                "machine": self.about_os(),
                "memory": self.total_memory(),
                "cpu": self.cpu_info(),
                "disk": self.disk_info(),
            }
        }

    def about_os(self):
        return {
            "Platform": self.os.system,
            "Machine Name": self.os.node,
            "Release": self.os.release,
            "Version": self.os.version,
            "Architecture": self.os.machine,
        }

    def total_memory(self):
        mem = virtual_memory()
        return f"{mem.total / 1024 / 1024:.1f}Mb"

    def cpu_info(self):
        return {
            "Physical Cores": cpu_count(logical=False),
            "Threads": cpu_count(logical=True),
        }

    def disk_info(self):
        usage = disk_usage("/")
        return f"{usage.total / 1000 / 1000 / 1000:.1f}Gb"
