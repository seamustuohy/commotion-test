import unittest
import subprocess
import sys
import os, time  #setUp and tearDown requirements
from util import ssh
from util import get_target

def start_iperf(host):
    start = ssh.ssh("root", host, "iperf -sD > /dev/null 2>&1")
def stop_iperf(host):
    stop = ssh.ssh("root", host, "kill -9 `pgrep iperf`")
class testFunctions(unittest.TestCase):

    def setUp(self):
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir("logs/"+date_string+"("+str(num+1)+")"):
            num += 1
            metric_dir = "logs/"+date_string+"("+str(num)+")"
        self.log = open(metric_dir+"/iperf", "a")
        self.log.write(time.strftime("Test Time: %Y-%m-%d %H:%M:%S") + "\n")
    def tearDown(self):
        self.log.close()
    def test_iperf(self):
        fail = False
        network_devices = get_target.get_all()
        for device in network_devices:
	    self.log.write("Destination: " + device[1] + "\n")
            start_iperf(device[1])
            traceroute = subprocess.Popen(["traceroute", "-n", device[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            iperf = subprocess.Popen(["iperf", "-c", device[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.log.write(traceroute.communicate()[0])
            self.log.write(iperf.communicate()[0])
            stop_iperf(device[1])
        self.assertFalse(fail)

