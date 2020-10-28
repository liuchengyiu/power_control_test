import os
import subprocess
from time import sleep
red_high = '\033[1;31m'
end = '\033[0m'
green_high = '\033[1;32m'
red = '\033[0;31m'
green = '\033[0;32m'
fail = 'fail'
success = 'success'

def run_shell(shell, code="utf8"):
    process = subprocess.Popen(shell, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = ""
    while process.poll() is None:
        line = process.stdout.readline()
        line = line.strip()
        if line:
            result = result + line.decode(code, 'ignore') + "\r\n"
    return result

def get_format_test_str(test):
    result = 'Result:{} {} {} message:{} {} {}'
    if test['flag'] == False:
        return result.format(red_high, fail, end, red, test['message'], end)
    return result.format(green_high, success, end, green, test['message'], end)