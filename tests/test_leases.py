import unittest
import subprocess
import sys
import os, time  #setUp and tearDown requirements
from util import ssh
from util import get_target

class testFunctions(unittest.TestCase):

    def setUp(self):
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir("logs/"+date_string+"("+str(num+1)+")"):
            num += 1
            metric_dir = "logs/"+date_string+"("+str(num)+")"
        self.log = open(metric_dir+"/leases", "a")
        self.log.write(time.strftime("Test Time: %Y-%m-%d %H:%M:%S") + "\n")

    def tearDown(self):
        self.log.close()

    def test_get_leases(self):
        fail = False
        network_devices = get_target.get_all()
        for device in network_devices:
            output = ssh.ssh("root", device[1], "ndsctl status")
            self.log.write(output)
        self.assertFalse(fail)

    
