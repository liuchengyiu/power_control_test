import os 
import subprocess
def run_shell(shell, code="utf8"):
    process = subprocess.Popen(shell, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ""
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            result = result + line.decode(code, 'ignore') + "\r\n"
    return result