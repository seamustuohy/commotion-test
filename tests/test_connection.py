import unittest
import subprocess
import os, time  #setUp and tearDown requirements
from . import ssh


class testFunctions(unittest.TestCase):

    def setUp(self):
        config = open("../config", "r")
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir("logs/"+date_string+"("+str(num+1)+")"):
            num += 1
            metric_dir = "logs/"+date_string+"("+str(num)+")"
        self.log = open(metric_dir+"/connection", "a")

    def tearDown(self):
        self.log.close()

    def test_ping_time(self):
        destinations = ["8.8.8.8", "127.0.0.1"]
        print("working")
        for ping_dest in destinations:
            ping = subprocess.Popen(["ping", "-c", "4", ping_dest], stdout=subprocess.PIPE)
            tail = subprocess.Popen(["tail", "-1"], stdin=ping.stdout, stdout=subprocess.PIPE)
            awk = subprocess.Popen(["awk", "{print $4}"], stdin=tail.stdout, stdout=subprocess.PIPE)
            cut = subprocess.Popen(["cut", "-d", "/",  "-f", "2"], stdin=awk.stdout, stdout=subprocess.PIPE)
            result = cut.communicate()[0]
            result=float(result[0:-1]) #remove the new line
            self.log.write("Average ping time to "+ping_dest+" "+str(result)+"\n")
        #assert it is not instant :) e.g. were getting a result 
            self.assertGreater(result, 0)



    
