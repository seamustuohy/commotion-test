import unittest
import subprocess
import sys
import os, time  #setUp and tearDown requirements
#from threading import Thread #only needed for stress test
from util import ssh
from util import get_target
from util import stress

def start_iperf(host):
    start = ssh.ssh("root", host, "iperf --server --daemon --udp > /dev/null 2>&1")

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
            iperf = subprocess.Popen(["iperf", "--client", "--udp", device[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.log.write(traceroute.communicate()[0])
            self.log.write(iperf.communicate()[0])
            stop_iperf(device[1])
        self.assertFalse(fail)

#The following is the stress tests... they may not be appropriate.
"""
class testStressFunctions(unittest.TestCase):

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

    def run_iperf(self, device, other=None):
        self.log.write("Destination: " + device[1] + "\n")
        start_iperf(device[1])
        traceroute = subprocess.Popen(["traceroute", "-n", device[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        iperf = subprocess.Popen(["iperf", "-c", device[1]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.log.write(traceroute.communicate()[0])
        self.log.write(iperf.communicate()[0])
        stop_iperf(device[1])
        
    def test_iperf(self):
        network_devices = get_target.get_all()
        files = get_target.get_all("test_files")
        for device in network_devices:
            for stress_num in stress.stressors:
                self.log.write("Stress Testing")
                self.log.write(str(stress_num)+" of wget processes")
                for f_loc in files:
                    t1 = Thread(target=self.run_iperf, args=(device[1], ""))
                    t2 = Thread(target=stress.stress_network, args=(stress_num, f_loc[1]))
                    t1.start()
                    t2.start()
                    t1.join()
                    t2.join()
                    
"""
