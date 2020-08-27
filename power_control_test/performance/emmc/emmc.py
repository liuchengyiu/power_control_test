from lib import run_shell

def deal_shell(shell_str):
    if shell_str.find("/s") == -1:
        return -1
    
    for line in shell_str.split("\r\n"):
        unit = 1
        if line.find("copied") == -1:
            continue
        speed = float(line[line.rfind(",")+1: line.find("/s")-2].strip())
        if line.find("MB") > 0:
            unit = 1000
        if line.find("KB") > 0 or line.find("kB") > 0:
            unit = 1000000
        speed = speed / unit
        return speed

def emmc_speed(d):
    result = []
    standard = d["speed"]
    shell_result = run_shell("dd if=/dev/zero of=file bs=1M count=1024")
    run_shell("rm -rf file")
    speed = deal_shell(shell_result)
    if speed == -1:
        result.append({
            "flag": False,
            "message": "Emmc speed test 执行失败"
        })
    if speed < standard:
        result.append({
            "flag": False,
            "message": "Emmc speed is {} GB/s".format(str(speed))
        })
    if speed >= standard:
        result.append({
            "flag": True,
            "message": "Emmc speed is {} GB/s".format(str(speed))
        })
    return result