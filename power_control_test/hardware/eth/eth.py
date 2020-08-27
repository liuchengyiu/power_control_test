from lib import run_shell
import re
def deal_shell(shell_result):
    if shell_result.find("/s") == -1:
        return -1
    for line in shell_result.split("\r\n"):
        if line.find("/s") == -1:
            continue;
        ds = re.split(' *', line.strip());
        return float(ds[len(ds)-2])

def eth_speed(d):
    serverip = d["serverip"]
    standard = d["speed"]
    result = []
    command = "./bin/iperf -c " + serverip + " -f m"
    shell_result = run_shell(command)
    print(shell_result);
    speed = deal_shell(shell_result)
    if speed == -1:
        result.append({
            "flag": False,
            "message": "Eth speed test 执行失败"
        })
    if speed < standard:
        result.append({
            "flag": False,
            "message": "Eth speed is {} Mb/s".format(str(speed))
        })
    if speed >= standard:
        result.append({
            "flag": True,
            "message": "Eth speed is {} Mb/s".format(str(speed))
        })
    return result