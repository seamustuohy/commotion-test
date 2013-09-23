import unittest
import os, time  #setUp and tearDown requirements

class testFunctions(unittest.TestCase):

    def setUp(self):
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir("logs/"+date_string+"("+str(num+1)+")"):
            num += 1
            metric_dir = "logs/"+date_string+"("+str(num)+")"
        self.log = open(metric_dir+"/QOS", "a")

    def tearDown(self):
        self.log.close()
