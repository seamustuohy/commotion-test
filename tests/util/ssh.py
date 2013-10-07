import subprocess

def ssh(user, host, command):
    process = subprocess.Popen(["ssh", user+"@"+host, command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,stderr = process.communicate()
    status = process.poll()
    return output

def scp(user, host, to_file, location):
    process = subprocess.Popen(["scp", to_file ,user+"@"+host+":"+location], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,stderr = process.communicate()
    status = process.poll()
    return output
