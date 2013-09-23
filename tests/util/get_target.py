
def get_all(location=None):
    if location == None:
        lines = [line.strip("\n") for line in open('config', 'r')]
    else:
        lines = [line.strip("\n") for line in open(location, 'r')]
    devices = []
    for i in lines:
        devices.append(i.split("="))
    return devices
