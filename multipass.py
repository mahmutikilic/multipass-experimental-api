import json
import subprocess
from haikunator import Haikunator


def _run_cmd(args):
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def generate_name():
    return Haikunator().haikunate(token_length=0)


def list_instances():
    out = _run_cmd(["multipass", "list", "--format", "json"])
    return json.loads(out)


def find_images():
    out = _run_cmd(["multipass", "find", "--format", "json"])
    return json.loads(out)


def launch_instance(name=None, cpu=None, disk=None, mem=None, image=None):
    name = name or generate_name()
    cmd = ["multipass", "launch", "-n", name]
    if cpu:
        cmd += ["-c", str(cpu)]
    if disk:
        cmd += ["-d", disk]
    if mem:
        cmd += ["-m", mem]
    if image:
        cmd.append(image)
    _run_cmd(cmd)
    return name


def get_version():
    return _run_cmd(["multipass", "version"]).strip()
