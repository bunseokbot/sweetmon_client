"""Install script for sweetmon client."""
from config import FUZZERINFO, save_config
from sweetmon import Fuzzer
import getpass

##########################################################
# Register
##########################################################
if FUZZERINFO["token"] is None:
    f = Fuzzer()
    password = getpass.getpass()

    token = f.register(password)
    if not token:
        print("[-] Could not register on server.")
        exit(-1)
    else:
        FUZZERINFO["token"] = token
        f.set_fuzzerinfo(FUZZERINFO)
        save_config(FUZZERINFO)
else:
    exit(1)
