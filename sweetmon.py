"""sweetmon client."""

from config import GLOBALINFO, FUZZERINFO
import requests
import json
import inspect
import threading

# Server URL configuration
URL = GLOBALINFO["SERVER_PROTOCOL"] + GLOBALINFO["SERVER_URL"]
URL_FUZZ = URL + "/fuzz"
URL_UPLOAD = URL + "/fuzz/crash"
URL_PING = URL + "/fuzz/ping"
URL_MACHINE = URL + "/machine"
URL_REGISTER = URL + "/fuzz/register"

# Default POST header.
HEADER = {
    "Cookie": "csrftoken=sweetfuzz",
    "X-CSRFTOKEN": "sweetfuzz",
    "Referer": URL
}


class Fuzzer(object):
    """Sweetfuzz fuzzer class."""

    def __init__(self):
        """Construct Fuzzer class."""
        self.fuzzerinfo = FUZZERINFO
        self.token = FUZZERINFO["token"]
        self.current_path = FUZZERINFO["current_path"]

        # Fuzzer testcase and crash count
        self.testcases = 0
        self.crashes = 0

    def count_testcase(self):
        """Count testcases."""
        return self.testcases

    def count_crash(self):
        """Count crashes."""
        return self.crashes

    def set_fuzzerinfo(self, fuzzerinfo):
        """Update fuzzerinfo."""
        self.fuzzerinfo = fuzzerinfo
        self.token = fuzzerinfo["token"]
        self.current_path = fuzzerinfo["current_path"]

    def send_machineinfo(self):
        """Send machine information to server."""
        data = {"INFO": json.dumps(self.fuzzerinfo)}
        self.post_data(URL_MACHINE, data)

    def ping(self):
        """Send ping to server."""
        try:
            data = {"token": self.token}
            result = self.post_data(URL_PING, data).text
            if result == "Done!":
                return True
        except Exception as e:
            print("[*] Error at %s" % inspect.stack()[0][3], e)
            return False

    def ping_thread(self):
        """Send ping thread 60 seconds."""
        print("[*] Tick ..")
        self.ping()
        threading.Timer(60, self.ping_thread).start()
        return True

    def upload_file(self, title, crashlog, filename):
        """Upload crashfile to server."""
        data = {"token": self.token, "crashlog": crashlog, "title": title}
        fdata = {'file': open(filename, 'rb')}
        self.post_data(URL_UPLOAD, data=data, files=fdata)

    def register(self, password):
        """Register fuzzer info server."""
        data = {
            "userkey": password,
            "fuzzer_name": self.fuzzerinfo["name"],
            "pub_ip": self.fuzzerinfo["machine"]["public_ip"],
            "pri_ip": self.fuzzerinfo["machine"]["private_ip"],
            "target": self.fuzzerinfo["target"]
        }

        result = self.post_data(URL_REGISTER, data).text

        if len(result) == 40:
            print("[*] Success, Your token is : " + result)
            return result

        return False

    def post_data(self, url, data, header=HEADER, **kwargs):
        """POST Data to server."""
        return requests.post(url, headers=header, data=data, **kwargs)
