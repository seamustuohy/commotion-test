import subprocess

def ssh(user, host, command):
    process = subprocess.Popen(["ssh", user+"@"+host, command], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output,stderr = process.communicate()
    status = process.poll()
    return output
