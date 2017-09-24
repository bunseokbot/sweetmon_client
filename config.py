"""sweetmon client configuration read-write file."""

import requests
import platform
import getpass
import socket
import json
import os

# Configuration JSON filename
filename = "config.json"

# Is client mode is debugging
debug = True

# Fuzzer Information
FUZZER_NAME = ""  # Name of fuzzer
FUZZING_TARGET = ""  # Target application
SERVER_URL = ""  # sub.domain.com
SERVER_PROTOCOL = ""  # https:// or http://

# If user set as debug mode
if debug:
    FUZZER_NAME = "TESTFUZZ"
    FUZZING_TARGET = "TESTTARGET"
    SERVER_URL = "localhost:8000"
    SERVER_PROTOCOL = "http://"


# Server Information
GLOBALINFO = {
    "SERVER_URL": SERVER_URL,
    "SERVER_PROTOCOL": SERVER_PROTOCOL,
    "TIME_PING": 60  # Second
}


# !WARNING! Do not modify this configuration
# Fill Automatic
FUZZERINFO = {
    "name": FUZZER_NAME,
    "target": FUZZING_TARGET,
    "owner": "",
    "current_path": "",
    "token": "",
    "machine": {
        "os": None,
        "public_ip": "",
        "private_ip": "",
    },
}

# Information of fuzzer and server
INFO = {"GLOBALINFO": GLOBALINFO, "FUZZERINFO": FUZZERINFO}


class Machine(object):
    """Get information of machine."""

    def __init__(self, fuzzerinfo):
        """Contstruct Machine class."""
        self.os = self.set_osinfo()
        self.public_ip = self.set_public_ip()
        self.private_ip = self.set_private_ip()
        self.current_path = self.set_current_path()
        self.username = self.set_username()
        self.fuzzerinfo = fuzzerinfo
        self.token = None

    def set_osinfo(self):
        """Set Operation System information."""
        return "{} {}".format(platform.system(), platform.release())

    def get_osinfo(self):
        """Get Operation System information."""
        return self.os

    def set_public_ip(self):
        """Set machine public ip address."""
        host = "http://httpbin.org/ip"
        try:
            req = requests.get(host).text
            return json.loads(req)['origin']
        except:
            print("Could not get IP from {} (Check your internet connection)"
                  .format(host))
            return None

    def get_public_ip(self):
        """Get machine public ip address."""

    def set_private_ip(self):
        """Set machine private ip address."""
        host = "httpbin.org"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 80))
            private_ip = s.getsockname()[0]
            s.close()
            return private_ip
        except:
            print("Could not get Private IP address from {}".format(host))
            return None

    def get_private_ip(self):
        """Get machine private ip address."""
        return self.private_ip

    def set_current_path(self):
        """Set current path."""
        return os.path.dirname(os.path.abspath(__file__))

    def get_current_path(self):
        """Get current path."""
        return self.current_path

    def set_username(self):
        """Set machine username."""
        return getpass.getuser()

    def get_username(self):
        """Get machine username."""
        return self.username

    def get_token(self):
        """Get machine token."""
        return self.token

    def set_token(self, token):
        """Set new updated token."""
        self.token = token
        self.update()

    def check_token(self):
        """Check token exist."""
        if self.token is None:
            return False
        return True

    def update_info(self):
        """Update machine information."""
        self.set_osinfo()
        self.set_public_ip()
        self.set_private_ip()
        self.set_username()
        self.set_current_path()

        # Update fuzzer information
        self.fuzzerinfo["owner"] = self.username
        self.fuzzerinfo["current_path"] = self.current_path
        self.fuzzerinfo["machine"]["os"] = self.os
        self.fuzzerinfo["machine"]["public_ip"] = self.public_ip
        self.fuzzerinfo["machine"]["private_ip"] = self.private_ip

        self.fuzzerinfo["token"] = self.token


def load_config():
    """Load configuration file."""
    with open(filename) as f:
        return json.loads(f.read())


def save_config(fuzzer):
    """Save configration setting info file."""
    with open(filename, "w") as f:
        f.write(json.dumps(fuzzer, indent=4))


requirements = [FUZZER_NAME, FUZZING_TARGET, SERVER_URL, SERVER_PROTOCOL]

# Check null value in requirements variable
if None in requirements:
    print("[*] Please fill blank variable.")
    exit(-1)

# Check Config file
if not os.path.exists(filename):
    print("[*] Create new Configuration file")

    machine = Machine(FUZZERINFO)
    machine.update_info()

    save_config(machine.fuzzerinfo)
else:
    FUZZERINFO = load_config()
