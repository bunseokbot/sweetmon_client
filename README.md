# SWEETMON-client

This project is a python module to interact with '[SWEETMON](https://github.com/sweetchipsw/sweetmon)' project.

Fuzz testers can adapt their fuzzer easily.

## Fast Install & Usage

### Prerequirement

- You should install sweetmon first to use this project. 
- Sweetmon : https://github.com/sweetchipsw/sweetmon
- Install Python3
  - Download python3 at http://python.org/ on Windows
  - ```apt-get install python3``` on Linux.
- Install Python package
  - ```pip3 install requests```

### Clone project

- ```git clone http://github.com/sweetchipsw/sweetmon-client```



### Get token from sweetmon

1. Please fill the contents in config.py. (Important)

   ```python
    FUZZER_NAME = ""  # Name of fuzzer
    FUZZING_TARGET = ""  # Target application
    SERVER_URL = ""  # sub.domain.com
    SERVER_PROTOCOL = ""  # https:// or http://
   ```

2. Run install.py

3. ```shell
   $ python install.py
   [*] Create new Configuration file
   [*] Input your userkey to access SWEETMON.. (You can find your key at your profile)
   Password:
   [*] Success, Your token is : d9a93042e67459df842c3b429a742790b805c056
   ```

4. Now you can adapt sweetmon-client for your fuzzer.



## Example

1. Simple Test

   ```python
    from sweetmon import Fuzzer

    # Test PING
    print("START TEST / LOAD CONFIG")

    f = Fuzzer()
    # print("TEST AUTO PING", F.RunPingThread())
    print("TEST PING", f.ping())
    print("TEST UPLOAD", f.upload_file("test", "here\nis_l0g", "config.json"))
    print("END OF TEST..")
   ```

   ​

## Files

* config.py : Configuration file.
* install.py : Install dependencies and regist fuzzer to the server.
* sweetmon.py : Core script / API 



### Information

```json
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
```

 