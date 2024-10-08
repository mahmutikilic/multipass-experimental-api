import logging
import subprocess
from haikunator import Haikunator
import os
import json
from loadconfig import Config
from dotenv import load_dotenv
from typing import Optional


def instacenaming():
    if Config.INST_USE_SPEC_CHAR == 0:
        match Config.INST_NAMING:
            case 1:
                return (Haikunator().
                haikunate(
                    token_length=0
                ))
            case 2:
                return (Haikunator().
                haikunate(
                    token_length=0,
                    token_chars=Config.INST_CUSTOM_NAME
                    ))
            case 3:
                return (Haikunator()
                .haikunate(
                    token_length=4
                ))
    elif Config.INST_USE_SPEC_CHAR == 1:
        match configparam:
            case 1:
                return (Haikunator()
                        .haikunate(
                    token_length=0,
                    delimiter=Config.INST_SPEC_CHAR
                ))
            case 2:
                return (Haikunator().
                        haikunate(
                    token_length=0,
                    token_chars=Config.INST_CUSTOM_NAME,
                    delimiter=Config.INST_SPEC_CHAR
                                              ))
            case 3:
                return (Haikunator()
                        .haikunate(
                    token_length=4
                ))
    elif Config.INST_USE_SPEC_CHAR != 1 or \
        Config.INST_USE_SPEC_CHAR != 0:
        logging.error("mea.ini/USE_SPEC_CHAR value is not set correctly! continue with default value (0)")
        return (Haikunator().
        haikunate(
            token_length=0
        ))




class Serverside:
    def __init__(self, vm_name, multipass_cmd="multipass"):
        self.cmd = multipass_cmd
        self.vm_name = vm_name
    def info(self):
        cmd = [self.cmd, "info", self.vm_name, "--format", "json"]
        out = subprocess.Popen(cmd,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        exitcode = out.wait()
        if(not exitcode == 0):
            raise Exception("Multipass info command failed: {0}".format(stderr))
        return json.loads(stdout)
    def delete(self):
        cmd = [self.cmd, "delete", self.vm_name]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Error deleting Multipass VM {0}".format(self.vm_name))
    def shell(self):
        raise Exception("The shell command is not supported in the Multipass SDK. Consider using exec.")
    def exec(self, cmd_to_execute):
        cmd = [self.cmd, "exec", self.vm_name]
        cmd += cmd_to_execute.split(" ")
        out = subprocess.Popen(cmd,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        exitcode = out.wait()
        if(not exitcode == 0):
            raise Exception("Multipass exec command failed: {0}".format(stderr))
        return stdout, stderr
    def stop(self):
        cmd = [self.cmd, "stop", self.vm_name]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Error stopping Multipass VM {0}".format(self.vm_name))
    def start(self):
        cmd = [self.cmd, "start", self.vm_name]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Error starting Multipass VM {0}".format(self.vm_name))
    def restart(self):
        cmd = [self.cmd, "restart", self.vm_name]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Error restarting Multipass VM {0}".format(self.vm_name))

    def version(self):
        cmd = [self.cmd, "version"]
        try:
            runcommand = subprocess.run(args=cmd,capture_output=True,check=True)
            if runcommand.returncode == 0:
                return json.loads(
                    runcommand.strout
                )
            else:
                logging.error("multipass version could't find")
        except json.JSONDecodeError as error:
            logging.error(error)



class ClientSide:
    """
    Multipass client
    """
    def __init__(self, multipass_cmd="multipass"):
        self.cmd = multipass_cmd
    def launch(self,
               vm_name=None,
               cpu=Config.DEFAULT,
               disk=Config.DEF_DISK_SIZE,
               mem=Config.DEF_MEM_SIZE,
               image=Config.DEF_BASE_IMAGE,
               cloud_init=Config.DEF_CLOUD_INIT
               ):
        if(not vm_name):
            # similar to Multipass's VM name generator
            vm_name = instacenaming()
        cmd = [self.cmd, "launch", "-c", str(cpu), "-d", disk, "-n", vm_name, "-m", mem]
        if(cloud_init):
            cmd.append("--cloud-init")
            cmd.append(cloud_init)
        if(image and not image == "ubuntu-lts"):
            cmd.append(image)
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Error launching Multipass VM {0}".format(vm_name))
        return MultipassVM(vm_name, self.cmd)
    def transfer(self, src, dest):
        cmd = [self.cmd, "transfer", src, dest]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Multipass transfer command failed.")
    def get_vm(self, vm_name):
        return MultipassVM(vm_name, self.cmd)
    def purge(self):
        cmd = [self.cmd, "purge"]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Purge command failed.")
    def list(self):
        cmd = [self.cmd, "list", "--format", "json"]
        out = subprocess.Popen(cmd,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        exitcode = out.wait()
        if(not exitcode == 0):
            raise Exception("Multipass list command failed: {0}".format(stderr))
        return json.loads(stdout)
    def find(self):
        cmd = [self.cmd, "find", "--format", "json"]
        out = subprocess.Popen(cmd,
           stdout=subprocess.PIPE,
           stderr=subprocess.STDOUT)
        stdout,stderr = out.communicate()
        exitcode = out.wait()
        if(not exitcode == 0):
            raise Exception("Multipass find command failed: {0}".format(stderr))
        return json.loads(stdout)
    def mount(self, src, target):
        cmd = [self.cmd, "mount", src, target]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Multipass mount command failed.")
    def unmount(self, mount):
        cmd = [self.cmd, "unmount", mount]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Multipass unmount command failed.")
    def recover(self, vm_name):
        cmd = [self.cmd, "recover", vm_name]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Multipass recover command failed.")
    def suspend(self):
        cmd = [self.cmd, "suspend"]
        try:
            subprocess.check_output(cmd)
        except:
            raise Exception("Multipass suspend command failed.")


class OJP: # Object JSON Parser
