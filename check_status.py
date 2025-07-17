import shutil


def multipass_exists():
    """Return True if the multipass command is available"""
    return shutil.which("multipass") is not None
