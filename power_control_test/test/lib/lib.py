import os
import subprocess, struct
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

def twoBcd_to_16(bate: str) -> str:
    bate_high= bate[:4]
    bate_low = bate[4:]
    bate= hex(int(bate_high, 2)).replace("0x", "")+ hex(int(bate_low, 2)).replace("0x", "")
    bate= ten_to_16(51+ sixteen_to_10(bate))
    if len(bate) == 1:
        bate = "0"+ bate
    return bate

def sixteen_to_10(bate: str) -> int:
    if bate == "":
        return 0
    bate = int(bate, 16)
    return bate
def ten_to_16(bate: int) -> str:
    bate= hex(bate).replace("0x", "")
    if len(bate) == 1:
        bate = "0" + bate
    return bate

def ten_to_2(bate: int) -> str:
    bate = bin(bate).replace("0b", "")
    for i in range(3):
        if len(bate) <4:
            bate= "0"+ bate
    return bate

def int4_to_float(array) -> float:
    data = bytearray()
    if len(array) < 4:
        return False
    for i in range(4):
        if array[i] >= 256:
            return False
        data.append(array[i])
    return struct.unpack("!f", data)[0]