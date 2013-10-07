import re
import os

def main(date=None, directory="logs"):
    """
    """
    if date == None:
        for root,dirs,files in os.walk(directory):
            for log in files:
                get_logs(directory, root, log)


def get_logs(root, directory, log):
    """
    """
    open(root+"/"+directory+"/"+log, "r")
    pass

def parse_connection():
    """
    """
    pass
    
def parse_leases():
    """
    """
    pass

def parse_iperf():
    """
    """
    pass

if __name__ == "__main__":
    main()
