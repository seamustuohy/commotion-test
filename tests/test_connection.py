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
        self.log = open(metric_dir+"/connection", "a")
        self.log.write(time.strftime("Test Time: %Y-%m-%d %H:%M:%S"))

    def tearDown(self):
        self.log.close()

    def test_ping_time(self):
        fail = False
        destinations = ["8.8.8.8", "127.0.0.1"]
        network_devices = get_target.get_all()
        for i in network_devices:
            destinations.append(i[1])
        for ping_dest in destinations:
            ping = subprocess.Popen(["ping", "-c", "4", ping_dest], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            tail = subprocess.Popen(["tail", "-1"], stdin=ping.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            awk = subprocess.Popen(["awk", "{print $4}"], stdin=tail.stdout, stdout=subprocess.PIPE, stderr=sys.stdout.fileno())
            test_set = awk.communicate()[0][0:-2]
            l = test_set.split("/")
            total = None
            if len(l) != 1:
                nums = [float(n) for n in l]
                total = sum(nums) / float(len(nums))
            if total:
                self.log.write("Average ping time to "+ping_dest+" was "+str(total)+" seconds\n")
            else:
                fail = True
                self.log.write(ping_dest+" could not be reached\n")
        self.assertFalse(fail)

    def test_sockets(self):
        network_devices = get_target.get_all()
        for device in network_devices:
            output = ssh.ssh("root", device[1], "netstat --statistics")
            self.log.write(output)
        myNetStat = subprocess.Popen(["netstat", "--statistics"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.log.write(myNetStat.communicate()[0])

    def test_jsonInfo(self):
        network_devices = get_target.get_all()
        for device in network_devices:
            if device[0] == "node":
                output = ssh.ssh("root", device[1], "curl -d http://127.0.0.1:9090/all/")
                self.log.write(output)



         

        
#not being run
"""    def test_mesh_devices(self):
        fail = False
        awk = subprocess.Popen(["nmap", "-vv", "5.0.0.0/24"], stdin=tail.stdout, stdout=subprocess.PIPE, stderr=sys.stdout.fileno())
        self.assetFalse(fail)
"""
