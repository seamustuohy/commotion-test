import unittest
import subprocess


class testFunctions(unittest.TestCase):

    def test_ping_time(self):
        self.response_time = subprocess.call("ping -c 4 www.stackoverflow.com | tail -1| awk '{print $4}' | cut -d '/' -f 2")
        print response_time
        
