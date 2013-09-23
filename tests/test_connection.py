import unittest
import subprocess


class testFunctions(unittest.TestCase):

    def test_ping_time(self):
        ping = subprocess.Popen(["ping", "-c", "4", "www.stackoverflow.com"], stdout=subprocess.PIPE)
        tail = subprocess.Popen(["tail", "-1"], stdin=ping.stdout, stdout=subprocess.PIPE)
        awk = subprocess.Popen(["awk", "{print $4}"], stdin=tail.stdout, stdout=subprocess.PIPE)
        cut = subprocess.Popen(["cut", "-d", "/",  "-f", "2"], stdin=awk.stdout, stdout=subprocess.PIPE)
        result = cut.communicate()[0]
        print result
        
