import unittest
import os, time #setUp and tearDown requirements


class testFunctions(unittest.TestCase):

    def setUp(self):
	num = 1
        date_string = time.strftime("%Y-%m-%d")
	metric_dir = "logs/"+date_string+"("+str(num)+")"
	while os.path.isdir("logs/"+date_string+"("+str(num+1)+")"):
            num += 1
            metric_dir = "logs/"+date_string+"("+str(num)+")"
        self.log = open(metric_dir+"/load", "a")
        self.log.write(time.strftime("Test Time: %Y-%m-%d %H:%M:%S"))

    def tearDown(self):
        self.log.close()
    
    def test_throughput(self):
        """iperf """
        self.log.write("PINEAPPLE")
        pass
    
    def test_jitter(self):
        """ """
        self.log.write("PINEAPPLE")
        pass
    
    def test_overhead(self):
        self.log.write("PINEAPPLE")
        pass
    
    def test_congestion(self):
        self.log.write("PINEAPPLE")
        pass
    
    def test_capacity(self):
        self.log.write("PINEAPPLE")
        pass

    


