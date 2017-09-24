"""Test sweetmon client."""
from sweetmon import Fuzzer

# Test PING
print("START TEST / LOAD CONFIG")

f = Fuzzer()
# print("TEST AUTO PING", F.RunPingThread())
print("TEST PING", f.ping())
print("TEST UPLOAD", f.upload_file("test", "here\nis_l0g", "config.json"))
print("END OF TEST..")
